import json
import datetime
import pandas as pd
import numpy as np

from data_handling import convert_country_to_continent
from api_requests import camelcase_to_underscore
from marvin_auxiliary_functions import in_list, make_screen_vector

from useful_lists import LIST_OF_SCREENS, CUSTOMER_JOURNEY, APP_ID_DICT, GESTURE_CODES_MOBILE

utc_convert = datetime.datetime.utcfromtimestamp



def load_data(app, max_page=10, full=False):
    """Load data of anonymisedapp from cache"""
    
    app_id = APP_ID_DICT[app]

    if full==False:
        page = 1
        list_sessions = []
        while page <= max_page:
            with open('./cache/sessions_from_app_id_{}_page_{}.json'.format(app_id, page),'r') as f:
                sessions = json.load(f)
                list_sessions.extend(sessions['data'])
            page += 1

    else:
        with open('./cache/sessions_from_app_id_{}.json'.format(app_id),'r') as f:
            list_sessions = json.load(f['data'])


    df = pd.DataFrame(list_sessions)

    return df



def prepare_data(df, app):
    """Perform data preparation"""

    # conventionalize column names 
    df.columns = [camelcase_to_underscore(_s) for _s in df.columns]
    df.rename(columns={'timestamp': 'time_stamp', 'screenvideo': 'screen_video', 
                       'used_appversion': 'used_app_version'}, inplace=True)
    df['id'] = [_d['$id'] for _d in df['_id']]

    # calculate simple columns
    df['time_of_the_day'] = [int(utc_convert(_ts).strftime('%H')) for _ts in df['time_stamp']]
    df['time_formatted'] = df['time_stamp'].apply(utc_convert)
    df['country_name'] = [_d['country_name'] for _d in df['device_location']]
    df['country_code'] = [_d['country_code'] for _d in df['device_location']]
    df['weekday'] = [datetime.datetime.strptime(day, '%Y-%m-%d').weekday() for day in df['ymd']]
    df['continent'] = [convert_country_to_continent(code) if code not in ['unknown'] else 'unknown'
                       for code in df['country_code']]
    
    # what are device_run and device_run_names?

    # drop unnecessary columns and rows with no data in heatmap_timeline
    df = df.drop(['__v', '_id', 'device_location', 'date'], axis=1)
    df = df[df.first_activity.notnull()]

    # delete rows where total_time == 0 
    df = df[df.total_time != 0]

    # running calculations and create some new columns
    df = calculate_screen_information(df)
    # deprecated: df = calculate_customer_journey(df, app)
    df = calculate_interaction_information(df, app)

    return df


def separate_os(df, ios=True):
    """Subset dataset based on device_class to get only iOS sessions"""

    if ios:
        df_ios = df[df['device_class'].str.startswith('i')]
        return df_ios
    else:
        df_not_ios = df[~df['device_class'].str.startswith('i')]
        return df_not_ios



def calculate_screen_information(df):
    """Calculate screen information"""

    # extract screen information
    df['screens_visited'] = df['heatmap_timeline'].apply(lambda c: [i['an'] for i in c])
    # count how many screens an user viewed in 1 sessions
    df['screen_number'] = df['screens_visited'].apply(len)

    df['time_per_screen'] = df['total_time'] / df['screen_number']

    # scale screen_number and total_time in scale of 10, with values > threshold becomes 10
    # df['screen_score'] = scale_threshold(df['screen_number'], threshold_screen)
    # df['time_score'] = scale_threshold(df['total_time'], threshold_time)

    return df



def calculate_interaction_information(df, app):
    """Calculate number of interactions and viewtime for each screen in each session"""


    df['interaction_information'] = df['heatmap_timeline'].apply(extract_interaction_time_and_information)

    # Summing interaction_count from each screen to get total interaction number
    df['interaction_number'] = df['interaction_information'].apply(lambda c: [i['interaction_count'] for i in c]).apply(sum)

    return df



def extract_interaction_time_and_information(cell):
    """Make a list of interaction time and summary information about screens from heatmap_timeline"""

    alist = []
    for screen in cell:
        adict = {}
        infor_arr = np.array([ele[0:6] for ele in screen['cor']]) # drop information about coordinates

        def build_cor_arr(list_cor):
            cor_arr = []
            for ele in list_cor:
                if len(ele[6]) == 0:
                    cor_arr.append([ele[0], ele[1], ele[0], ele[1]])
                else:
                    cor_arr.append([ele[0], ele[1], ele[6][-1][-2], ele[6][-1][-1]])
            return np.array(cor_arr)

        cor_arr = build_cor_arr(screen['cor'])
    
        if infor_arr.ndim == 2:
            responsive = infor_arr[infor_arr[:,4] != 0] # drop non-responsive interactions
            cor_arr_res = cor_arr[infor_arr[:,4] != 0]

            if len(responsive) != 0: 
                time_arr = responsive[:,5]
                gesture_arr = responsive[:,3]
                orientation_arr = responsive[:,2]
                
                # use the time array to remove swipe-trail recording issue (swipe time > trail time)
                true_arr = np.append([np.diff(time_arr) > 0],[True])
                true_time_arr = time_arr[true_arr]
                true_gesture_arr = gesture_arr[true_arr]
                true_coor_arr = cor_arr_res[true_arr]
                true_orientation_arr = orientation_arr[true_arr]

            else:
                true_time_arr, true_gesture_arr, true_coor_arr, true_orientation_arr = [], [], [], []

        elif (infor_arr.ndim == 1) and (len(infor_arr) > 1) and (infor_arr[4] != 0):
            true_time_arr = [infor_arr[5]]
            true_gesture_arr = [infor_arr[3]]
            true_coor_arr = cor_arr
            true_orientation_arr = [infor_arr[2]]
        else:
            true_time_arr, true_gesture_arr, true_coor_arr, true_orientation_arr = [], [], [], []

        adict['_screen'] = screen['an'] # use _screen (with _) to ensure it appears first when print
        adict['interaction_count'] = len(true_time_arr)
        adict['interaction_times'] = np.array(true_time_arr)
        adict['interaction_labels'] = [GESTURE_CODES_MOBILE[i] for i in true_gesture_arr]
        adict['interaction_coors'] = np.array(true_coor_arr)
        adict['orientations'] = np.array(true_orientation_arr)
        adict['start_time'] = screen['at']
        adict['view_time'] = screen['vt']

        alist.append(adict)

    return alist



####### DEPRECATED #######



def calculate_customer_journey(df, app):
    """Calculate 4 stages in the journey in each session"""

    # count how many times an user viewed a screen belonging to a stage, in 1 session
    if app in CUSTOMER_JOURNEY.keys():
        for stage in CUSTOMER_JOURNEY[app].keys():
            column_stage_name = stage + '_stage'
            df[column_stage_name] = df['screens_visited'].apply(in_list, list_of_items = CUSTOMER_JOURNEY[app][stage])

    return df