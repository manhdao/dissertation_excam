import json
import pandas as pd 
import datetime
import numpy as np
from pycountry_convert import convert_country_alpha2_to_continent
from data_handling import utc_convert
import matplotlib.dates as mdates
import scipy

import seaborn as sns
import matplotlib.pyplot as plt
plt.switch_backend('agg')

# CLustering
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score, fowlkes_mallows_score, \
                            confusion_matrix, make_scorer
from sklearn.metrics import make_scorer

from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from marvin_algorithms import purity_score


from marvin_data_prep import load_data, prepare_data, separate_os

#data mining
from marvin_auxiliary_functions import timestamp_array, make_screen_vector, extract_interaction_sequence_selected_screen, \
                                       in_list,count_screen_in_sessions_data,distribution_cluster_result,build_overall_vector,\
                                       extract_orientation_selected_screen
from marvin_plot_functions import plot_confusion_matrix, plot_screen_timestamp_histogram_9, plot_screen_period_characteristics,\
                                  plot_screen_coordinates
from marvin_algorithms import dynamic_time_warp, condensed_matrix, distance_matrix, cross_distance_matrix, levenshtein
from useful_lists import important_screens, LIST_OF_SCREENS, ios_screens, ios_useful_screens, \
                            columns_name_quantization, columns_name_features, columns_simple, columns_name_4, columns_name_9, \
                            columns_name_no_other, columns_name_everything


if __name__ == '__main__':

    import time
    start_time = time.time()

    df = load_data('anonymisedapp', 150)
    df = prepare_data(df, 'anonymisedapp')
    df = separate_os(df)
    print(len(df))

    df_seq = extract_interaction_sequence_selected_screen(df, selected_screens=ios_useful_screens, coor_details=True)
    print(len(df_seq))

    df_ori = extract_orientation_selected_screen(df, selected_screens=ios_useful_screens)
    df_ori['non_portrait'] = df_ori['orientation_list'].apply(in_list, list_of_items = [0,2,3])
    index_non_portrait = df_ori[df_ori.non_portrait != 0].index

    df_seq.drop(index_non_portrait, inplace=True)

    df_seq['interaction_vector'] = 0.
    df_seq.loc[:,'interaction_vector'] = df_seq.apply(build_overall_vector, axis=1) # important


    df_quan = pd.DataFrame(df_seq['interaction_vector'].tolist(), columns = columns_name_quantization, index=df_seq.index)
    df_vq = pd.concat([df_seq[['session_id','user_id','time','screen']], df_quan], axis=1)
    # important
    df_vq['log_interactionnumber'] = np.log(df_vq.interaction_number)
    df_vq['log_viewtime'] = np.log(df_vq.viewtime)
    print(len(df_vq)

    seed = 1437
    number_row = 3000
    df_1 = df_vq[df_vq.screen == 'PhotoStreamViewController'].sample(n=number_row, random_state=seed)
    df_2 = df_vq[df_vq.screen == 'UploadViewController'].sample(n=number_row, random_state=seed)
    df_4 = df_vq[df_vq.screen == 'EventPageViewController'].sample(n=number_row, random_state=seed)
    df_3 = df_vq[df_vq.screen == 'GuestsViewController'].sample(n=number_row, random_state=seed)
    df_sample = pd.concat([df_1, df_2, df_3, df_4])
    print(len(df_sample))


    y = df_sample['screen']
    le = LabelEncoder()
    y_true = le.fit_transform(y)


    X = df_sample[columns_name_everything]

    scaler = MinMaxScaler()
    X_scale = scaler.fit_transform(X)
    print(X_scale.shape)

    del df
    del df_quan
    del df_vq
    del df_sample


    rf = RandomForestClassifier(max_depth = 15, n_estimators = 300, random_state = seed, oob_score=True)
    sfs = SFS(rf, 
           k_features=10, 
           forward=True, 
           floating=False, 
           verbose=2,
           scoring='accuracy',
           cv=3)
    sfs.fit(X_scale, y_true)

    print('SFS results')
    feature_index = list(sfs.k_feature_idx_)
    print(X.iloc[:,feature_index].columns)

    sbs = SFS(rf, 
           k_features=10, 
           forward=False, 
           floating=False, 
           verbose=2,
           scoring='accuracy',
           cv=3)
    sbs.fit(X_scale, y_true)

    print('SBS results')
    feature_index = list(sbs.k_feature_idx_)
    print(X.iloc[:,feature_index].columns)

    print("%f seconds" % (time.time() - start_time))



