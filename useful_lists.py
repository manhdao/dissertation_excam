APP_ID_DICT = {'anonymisedapp':'123'}

GESTURE_CODES_MOBILE = {0: 'single_tap',
                        1: 'double_tap',
                        2: 'swipe_up',
                        3: 'swipe_down',
                        4: 'swipe_left',
                        5: 'swipe_right',
                        6: 'scroll',                      # no interaction recorded
                        7: 'zoom_in',
                        8: 'zoom_out',
                        9: 'long_tap',                    # no interaction recorded
                        10: 'orientation_change_ios',
                        15: 'orientation_change_android', # skip
                        11: 'trail'
                        }

gesture_list_ios = ['single_tap',
 'double_tap',
 'swipe_up',
 'swipe_down',
 'swipe_left',
 'swipe_right',
 'scroll',
 'zoom_in',
 'zoom_out',
 'long_tap',
 'orientation_change_ios',
 # 'orientation_change_android', # skip this because we are working on iOS only
 'trail']


columns_name_quantization = ['interaction_number','hist4_1','hist4_2','hist4_3','hist4_4','hist9_1','hist9_2',   # 0-6
                             'hist9_3','hist9_4','hist9_5','hist9_6','hist9_7','hist9_8','hist9_9',              # 7-13
                             'tap','swipe','other',                                                              # 14-16
                             'bin1','bin4_tap_1','bin4_tap_2','bin4_tap_3','bin4_tap_4',                         # 17-21
                             'bin9_tap_1','bin9_tap_2','bin9_tap_3','bin9_tap_4','bin9_tap_5','bin9_tap_6',      # 22-27
                             'bin9_tap_7','bin9_tap_8','bin9_tap_9',                                             # 28-30
                             'bin4_swipe_1','bin4_swipe_2','bin4_swipe_3','bin4_swipe_4',                        # 31-34
                             'bin9_swipe_1','bin9_swipe_2','bin9_swipe_3','bin9_swipe_4','bin9_swipe_5',         # 35-39
                             'bin9_swipe_6','bin9_swipe_7','bin9_swipe_8','bin9_swipe_9',                        # 40-43
                             'bin4_other_1','bin4_other_2','bin4_other_3','bin4_other_4',                        # 44-47
                             'bin9_other_1','bin9_other_2','bin9_other_3','bin9_other_4','bin9_other_5',         # 48-52
                             'bin9_other_6','bin9_other_7','bin9_other_8','bin9_other_9','viewtime']             # 53-57

columns_name_features = columns_name_quantization + ['log_interactionnumber','log_viewtime']                     # 58-59


columns_simple = ['hist4_1','hist4_2','hist4_3','hist4_4',
                  'bin1','bin4_tap_1','bin4_tap_2','bin4_tap_3','bin4_tap_4',
                  'bin4_swipe_1','bin4_swipe_2','bin4_swipe_3','bin4_swipe_4',
                  'log_interactionnumber','log_viewtime']

columns_name_4 = ['hist4_1','hist4_2','hist4_3','hist4_4','tap','swipe','other',
                  'bin1','bin4_tap_1','bin4_tap_2','bin4_tap_3','bin4_tap_4',
                  'bin4_swipe_1','bin4_swipe_2','bin4_swipe_3','bin4_swipe_4', 
                  'bin4_other_1','bin4_other_2','bin4_other_3','bin4_other_4',
                  'log_interactionnumber','log_viewtime']

columns_name_9 = ['hist9_1','hist9_2','hist9_3','hist9_4','hist9_5','hist9_6','hist9_7','hist9_8','hist9_9',
                  'tap','swipe','other','bin1', 
                  'bin9_tap_1','bin9_tap_2','bin9_tap_3','bin9_tap_4','bin9_tap_5','bin9_tap_6', 'bin9_tap_7','bin9_tap_8','bin9_tap_9',
                  'bin9_swipe_1','bin9_swipe_2','bin9_swipe_3','bin9_swipe_4','bin9_swipe_5','bin9_swipe_6','bin9_swipe_7','bin9_swipe_8','bin9_swipe_9',
                  'bin9_other_1','bin9_other_2','bin9_other_3','bin9_other_4','bin9_other_5','bin9_other_6','bin9_other_7','bin9_other_8','bin9_other_9',
                  'log_interactionnumber','log_viewtime']

columns_name_no_other = ['hist4_1','hist4_2','hist4_3','hist4_4','hist9_1','hist9_2','hist9_3','hist9_4','hist9_5','hist9_6',
                         'hist9_7','hist9_8','hist9_9','tap','swipe','bin1','bin4_tap_1','bin4_tap_2','bin4_tap_3','bin4_tap_4',
                         'bin4_swipe_1','bin4_swipe_2','bin4_swipe_3','bin4_swipe_4','bin9_tap_1','bin9_tap_2','bin9_tap_3',
                         'bin9_tap_4','bin9_tap_5','bin9_tap_6', 'bin9_tap_7','bin9_tap_8','bin9_tap_9','bin9_swipe_1',
                         'bin9_swipe_2','bin9_swipe_3','bin9_swipe_4','bin9_swipe_5','bin9_swipe_6','bin9_swipe_7',
                         'bin9_swipe_8','bin9_swipe_9','log_interactionnumber','log_viewtime']


columns_name_everything = ['hist4_1','hist4_2','hist4_3','hist4_4','hist9_1','hist9_2','hist9_3','hist9_4','hist9_5','hist9_6',
                           'hist9_7','hist9_8','hist9_9','tap','swipe','other','bin1','bin4_tap_1','bin4_tap_2','bin4_tap_3',
                           'bin4_tap_4','bin4_swipe_1','bin4_swipe_2','bin4_swipe_3','bin4_swipe_4','bin4_other_1','bin4_other_2',
                           'bin4_other_3','bin4_other_4','bin9_tap_1','bin9_tap_2','bin9_tap_3','bin9_tap_4','bin9_tap_5',
                           'bin9_tap_6', 'bin9_tap_7','bin9_tap_8','bin9_tap_9','bin9_swipe_1',
                           'bin9_swipe_2','bin9_swipe_3','bin9_swipe_4','bin9_swipe_5','bin9_swipe_6','bin9_swipe_7',
                           'bin9_swipe_8','bin9_swipe_9','bin9_other_1',
                           'bin9_other_2','bin9_other_3','bin9_other_4','bin9_other_5','bin9_other_6','bin9_other_7',
                           'bin9_other_8','bin9_other_9','log_interactionnumber','log_viewtime']


list_of_columns = ['app_id',
 'app_version',
 'company_name',
 'crash_log',
 'device_class',
 'device_model_name',
 'device_id',
 'device_name',
 'device_run',
 'device_run_name',
 'device_run_notes',
 'device_type',
 'email',
 'events',
 'first_activity',
 'heatmap_timeline',
 'height',
 'is_crash',
 'is_favorite',
 'os_lname',
 'os_name',
 'os_name_float',
 'preferences',
 'resolution',
 'sdk_version',
 'tags',
 'time_stamp',
 'total_time',
 'unplayed',
 'used_app_version',
 'width',
 'ymd',
 'id',
 'time_of_the_day',
 'time_formatted',
 'country_name',
 'country_code',
 'weekday',
 'continent',
 'screens_visited',
 'screen_number',
 'time_per_screen',
 'screen_score',
 'time_score',
 'first_time_stage',
 'active_use_stage',
 'beneficial_action_stage',
 'photo_viewer_stage',
 'interaction_information',
 'interaction_number']


LIST_OF_SCREENS =['AboutViewController',
 'AdminViewController',
 'CameraViewController',
 'CommentViewController',
 'CouponModalViewController',
 'CreateProfileEmailViewController',
 'CreateProfileModalViewController',
 'CreateWeddingViewController',
 'DownloadViewController',
 'EditViewController',
 'EventPageViewController',
 'GeneralModalViewController',
 'GuestsViewController',
 'InvitationViewController',
 'MenuController',
 'PersonalInfoViewController',
 'PhotoStreamViewController',
 'ProfileSettingsViewController',
 'ProfileViewController',
 'PurchaseViewController',
 'QRCodeViewController',
 'RateViewController',
 'ScheduleTimeViewController',
 'ShareViewController',
 'SupportViewController',
 'TimeScheduleViewController',
 'UploadQueueTableViewController',
 'UploadViewController',
 'ViewController',
 'WeddingCodeViewController',#30
 'AVFullScreenPlaybackControlsViewController',
 'ImageViewer.GalleryViewController',
 'ImageViewer.ImageViewController',
 'MFMailComposeRemoteViewController',
 'SLRemoteComposeViewController',
 'UIActivityGroupViewController',
 'UIAlertController',
 'UIApplicationRotationFollowingControllerNoTouches',
 '_UIActivityUserDefaultsViewController',
 '_UIAlertControllerTextFieldViewController',
 '_UIRemoteInputViewController',#41
 'CommentActivity',
 'CreationActivity',
 'CropImageActivity',
 'FacebookActivity',
 'GotaActivity',
 'MainActivity',
 'PictureActivity',
 'ScanBarcodeActivity'] #49

ios_screens=['AboutViewController',
 'AdminViewController',
 'CameraViewController',
 'CommentViewController',
 'CouponModalViewController',
 'CreateProfileEmailViewController',
 'CreateProfileModalViewController',
 'CreateWeddingViewController',
 'DownloadViewController',
 'EditViewController',
 'EventPageViewController',
 'GeneralModalViewController',
 'GuestsViewController',
 'InvitationViewController',
 'MenuController',
 'PersonalInfoViewController',
 'PhotoStreamViewController',
 'ProfileSettingsViewController',
 'ProfileViewController',
 'PurchaseViewController',
 'QRCodeViewController',
 'RateViewController',
 'ScheduleTimeViewController',
 'ShareViewController',
 'SupportViewController',
 'TimeScheduleViewController',
 'UploadQueueTableViewController',
 'UploadViewController',
 'ViewController']


ios_useful_screens=['AboutViewController',
 'AdminViewController',
 'CameraViewController',
 'CommentViewController',
 'CouponModalViewController',
 'CreateProfileEmailViewController',
 'CreateProfileModalViewController',
 'CreateWeddingViewController',
 'DownloadViewController',
 'EditViewController',
 'EventPageViewController',
 'GuestsViewController',
 'InvitationViewController',
 'PersonalInfoViewController',
 'PhotoStreamViewController',
 'ProfileSettingsViewController',
 'ProfileViewController',
 'PurchaseViewController',
 'QRCodeViewController',
 'RateViewController',
 'ScheduleTimeViewController',
 'ShareViewController',
 'SupportViewController',
 'TimeScheduleViewController',
 'UploadQueueTableViewController',
 'UploadViewController']


full_set_of_screens = {'AVFullScreenPlaybackControlsViewController',
 'CommentActivity',
 'CreationActivity',
 'CropImageActivity',
 'FacebookActivity',
 'GotaActivity',
 'ImageViewer.GalleryViewController',
 'ImageViewer.ImageViewController',
 'MFMailComposeRemoteViewController',
 'MainActivity',
 'PictureActivity',
 'SLRemoteComposeViewController',
 'ScanBarcodeActivity',
 'UIActivityGroupViewController',
 'UIAlertController',
 'UIApplicationRotationFollowingControllerNoTouches',
 'AboutViewController',
 'AdminViewController',
 'CameraViewController',
 'CommentViewController',
 'CouponModalViewController',
 'CreateProfileEmailViewController',
 'CreateProfileModalViewController',
 'CreateWeddingViewController',
 'DownloadViewController',
 'EditViewController',
 'EventPageViewController',
 'GeneralModalViewController',
 'GuestsViewController',
 'InvitationViewController',
 'MenuController',
 'PersonalInfoViewController',
 'PhotoStreamViewController',
 'ProfileSettingsViewController',
 'ProfileViewController',
 'PurchaseViewController',
 'QRCodeViewController',
 'RateViewController',
 'ScheduleTimeViewController',
 'ShareViewController',
 'SupportViewController',
 'TimeScheduleViewController',
 'UploadQueueTableViewController',
 'UploadViewController',
 'ViewController',
 'WeddingCodeViewController',
 '_UIActivityUserDefaultsViewController',
 '_UIAlertControllerTextFieldViewController',
 '_UIRemoteInputViewController'}




####### DEPRECATED #######



important_screens = ['PhotoStreamViewController','DownloadViewController',
                    'PurchaseViewController','UIAlertController']

bins_dfc = [0,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700]


threshold_screen = 10.0 # This number should be independent of data,or updated periodically
threshold_time = 237.3 # This number should be independent of data,or updated periodically


CUSTOMER_JOURNEY = {'anonymisedapp':
                       {'first_time': 
                           ['CreateProfileEmailViewController',
                            'CreateProfileModalViewController'
                            ],
                        'photo_viewer': 
                           ['PhotoStreamViewController',
                            'DownloadViewController'
                            ],
                        'active_use': 
                           ['CameraViewController',
                            'UploadViewController'
                            ],
                        'beneficial_action':
                           ['PurchaseViewController',
                            'RateViewController',
                            'ShareViewController',
                            'InvitationViewController'
                            ]
                        }
                    }


