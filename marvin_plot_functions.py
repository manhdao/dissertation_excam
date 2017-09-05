import numpy as np
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
import itertools
from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score, fowlkes_mallows_score, confusion_matrix
from marvin_algorithms import purity_score

from useful_lists import GESTURE_CODES_MOBILE, important_screens, bins_dfc, gesture_list_ios


def plot_screen_period_characteristics(df, screen, xlim1, xlim2, type='sequence'):
    """Plot the distribution of characteristics of screen period.
    
    type: plot the pair of sequence hist_length and interaction_number, or the pair of 
                    swipe-tap inteaction. 'sequence' or 'swipe-tap'"""

    if type == 'sequence':
        x1, x2 = df.viewtime[df.screen == screen], \
                 df.interaction_number[df.screen == screen]
        # x1, x2 = df.hist_length[df.screen == screen], \
        #         df.interaction_number[df.screen == screen] for unequal
        label1, label2 = 'Viewtime', 'Interaction_number'

    elif type == 'swipe-tap':
        x1, x2 = df.swipe[df.screen == screen], \
                 df.tap[df.screen == screen]
        label1, label2 = 'Swipe', 'Tap'

    elif type == 'ratio':
        x1, x2 = df['interaction/length ratio'][(df.screen == screen) & (df['viewtime'] > 0)], \
                 df['swipe/tap ratio'][(df.screen == screen) & (df['tap'] > 0)]
        label1, label2 = 'Interaction/length ratio', 'Swipe/tap ratio'

    else:
        raise ValueError(type+ ' is not a correct choice. Choose from sequence, swipe-tap, or ratio')
    

    fig=plt.figure(figsize = [12, 4])

    ax1 = fig.add_subplot(1,2,1)
    ax1.hist(x1, bins=range(0,int(np.floor(max(x1)))+1))
    ax1.set_xlim(xlim1)
    ax1.set_xlabel(label1)
    ax1.set_ylabel('Frequency')
    ax1.set_title(screen+' period '+label1+\
                  '\nmean: '+str(np.mean(x1))+\
                  '\nvariance: '+str(np.var(x1)))
    
    ax2 = fig.add_subplot(1,2,2)
    ax2.hist(x2, bins=range(0,int(np.floor(max(x2)))+1), color='#ff81c0')
    ax2.set_xlim(xlim2)
    ax2.set_xlabel(label2)
    ax2.set_ylabel('Frequency')
    ax2.set_title(screen+' period '+label2+\
                  '\nmean: '+str(np.mean(x2))+\
                  '\nvariance: '+str(np.var(x2)))
    plt.show()



def plot_screen_coordinates(df, screen, bin=4):
    """Plot the distribution of the mean of interaction coordinates in a heatmap matrix"""
    
    if bin == 4:
        list_4bins = ['bin4_tap_1','bin4_tap_2','bin4_tap_3','bin4_tap_4',
                      'bin4_swipe_1','bin4_swipe_2','bin4_swipe_3','bin4_swipe_4']
        coors = df[df.screen == screen][list_4bins]
        
        mat_tap, mat_swipe = np.zeros([2,2]), np.zeros([2,2])
        
        k = 0
        for i in range(2):
            for j in range(2):
                mat_tap[i,j] = np.mean(coors[list_4bins[k]])
                mat_swipe[i,j] = np.mean(coors[list_4bins[k+4]])
                k += 1
        
        def plot_text(ax, mat, fontsize=15, threshold=1.3):
            k = 0
            threshold = threshold * np.mean(mat)
            for i in range(2):
                for j in range(2):
                    ax.text(j, i, str(k+1), fontsize=fontsize, 
                            color='white' if mat[i,j] > threshold else 'black')
                    ax.text(j-0.05, i+0.2, ('%.3f' % mat[i,j]), 
                            color='white' if mat[i,j] > threshold else 'black')
                    k += 1
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(None)

        fig=plt.figure(figsize = [8, 4])

        ax1 = fig.add_subplot(121)
        ax1.imshow(mat_tap, interpolation='nearest', cmap='Blues')
        plot_text(ax1, mat_tap)
        ax1.set_title('Tap')

        ax2 = fig.add_subplot(122)
        ax2.imshow(mat_swipe, interpolation='nearest', cmap='YlOrRd')
        plot_text(ax2, mat_swipe)
        ax2.set_title('Swipe')

        plt.suptitle(screen)
        plt.show()

    if bin == 9:
        list_9bins = ['bin9_tap_1','bin9_tap_2','bin9_tap_3','bin9_tap_4','bin9_tap_5',      
                      'bin9_tap_6','bin9_tap_7','bin9_tap_8','bin9_tap_9',
                      'bin9_swipe_1','bin9_swipe_2','bin9_swipe_3','bin9_swipe_4','bin9_swipe_5',      
                      'bin9_swipe_6','bin9_swipe_7','bin9_swipe_8','bin9_swipe_9']
        coors = df[df.screen == screen][list_9bins]

        mat_tap, mat_swipe = np.zeros([3,3]), np.zeros([3,3])
        
        k = 0
        for i in range(3):
            for j in range(3):
                mat_tap[i,j] = np.mean(coors[list_9bins[k]])
                mat_swipe[i,j] = np.mean(coors[list_9bins[k+9]])
                k += 1
        
        def plot_text(ax, mat, fontsize=15, threshold=1.3):
            k = 0
            threshold = threshold * np.mean(mat)
            for i in range(3):
                for j in range(3):
                    ax.text(j, i, str(k+1), fontsize=fontsize, 
                            color='white' if mat[i,j] > threshold else 'black')
                    ax.text(j-0.05, i+0.2, ('%.3f' % mat[i,j]), 
                            color='white' if mat[i,j] > threshold else 'black')
                    k += 1
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(None)

        fig=plt.figure(figsize = [8, 4])

        ax1 = fig.add_subplot(121)
        ax1.imshow(mat_tap, interpolation='nearest', cmap='Blues')
        plot_text(ax1, mat_tap)
        ax1.set_title('Tap')

        ax2 = fig.add_subplot(122)
        ax2.imshow(mat_swipe, interpolation='nearest', cmap='YlOrRd')
        plot_text(ax2, mat_swipe)
        ax2.set_title('Swipe')

        plt.suptitle(screen)
        plt.show()




def plot_confusion_matrix(y_true, y_cluster, classes, normalize=False, type='clustering', cmap=plt.cm.Blues):
    """Plot the confusion matrix adn print some external metrics"""
    
    cm = confusion_matrix(y_true, y_cluster) # y_cluster is the same as y_pred

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    tick_marks = np.arange(len(classes))
    
    cluster_list = ['Cluster ' + str(i+1) for i in range(len(cm))]
    
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color='white' if cm[i, j] > thresh else 'black')

    print('Scores:')
    print('Purity: %.5f' % (purity_score(y_true, y_cluster)))
    print('AMI: %.5f' % (adjusted_mutual_info_score(y_true, y_cluster)))
    print('Rand Index: %.5f' % (adjusted_rand_score(y_true, y_cluster)))
    print('Fowlkes–Mallows index: %.5f' % (fowlkes_mallows_score(y_true, y_cluster)))

    plt.tight_layout()
    plt.grid(None)
    plt.title('Confusion matrix')
    plt.ylabel('True label', fontsize = 12)

    if type == 'clustering':
        plt.xlabel('Clusters', fontsize = 12)
        plt.xticks(tick_marks, cluster_list, rotation=45)
    elif type == 'classification':
        plt.xlabel('Predicted label', fontsize =12)
        plt.xticks(tick_marks, classes, rotation=45)

    plt.show()

        





def plot_screen_timestamp_histogram_9(df, screen):
    """Plot the distribution of the mean of interaction timestamp features"""

    list_9hists = ['hist9_1','hist9_2','hist9_3','hist9_4','hist9_5','hist9_6','hist9_7','hist9_8','hist9_9']
    times = df[df.screen == screen][list_9hists]

    arr = np.zeros([9,])

    for i in range(9):
        arr[i] = np.mean(times[list_9hists[i]])

    plt.bar(left=np.arange(9)+1, height=arr, color='#9acd32')
    plt.xticks(range(1,10), list_9hists, fontsize = 12, rotation=90)
    plt.title(screen)
    plt.show()





def plot_histogram_scaled(df,lower_bound, upper_bound, max=6, type='screen', 
                                bins='even', relative=False, **kwargs):
    """Ploting histogram of multiple sessions, from lower_bound to upper_bound"""

    number_sessions = upper_bound - lower_bound + 1
    fig=plt.figure(figsize = [16, 3 * (number_sessions // 4. + 1)])

    if bins == 'even':
        bins = np.linspace(0,1,11)
    elif bins == 'log':
        bins = np.concatenate((np.array([0]),np.geomspace(0.1,1,4)))
    else:
        bins = np.array(bins)
    
    j = 1
    for i in range(lower_bound, upper_bound+1):
        ax = fig.add_subplot((number_sessions // 4. + 1), 4, j)

        try:
            arr = timestamp_array(df.interaction_information[i], type=type)
            if relative == False:
                ax.hist(arr, bins=bins, rwidth=0.9, **kwargs)
                ax.set_ylim([0,max])
                ax.set_ylabel('Frequency')
            if relative == True:
                ax.hist(arr, bins=bins, weights=np.zeros_like(arr) + 1./arr.size,
                        rwidth=0.9, **kwargs)
                ax.set_ylim([0,1])
                ax.set_ylabel('Relative frequency')
            ax.set_title('Session '+ str(i))
        except:
            continue
        
        j += 1
    plt.tight_layout()
    plt.show()



def plot_time_vs_screen_vs_interaction(df,size=18):
    """Plot time vs screen distribution of sessions"""

    df2 = df[['screen_number', 'total_time', 'interaction_number']].copy()
    bins = [0,10,20,40,max(df2.interaction_number)+1]
    df2['interaction_bin'] = pd.cut(df2['interaction_number'], bins, labels =[1,2,3,4])
    df2['log_screen_number'] = np.log(df.screen_number)
    df2['log_total_time'] = np.log(df.total_time)

    df2 = df2.drop_duplicates()

    fig = plt.figure(figsize = [9,5])
    plt.scatter(x='screen_number', y='log_total_time', c='interaction_bin', s=size,
                                   cmap='plasma', edgecolor='b', data=df2)
    plt.xlabel('screen_number')
    plt.ylabel('log_total_time')
    plt.colorbar()
    plt.show()



def plot_trail(combo):
    """Plot trail and swipe initiation point from data of a swipe followed by a trail"""

    trail_arr = np.array(combo[1][6])
    x_cors = trail_arr[:,2:3].reshape(len(trail_arr))
    y_cors = trail_arr[:,-1].reshape(len(trail_arr))
    time_sequence = trail_arr[:,1:2].reshape(len(trail_arr))
    plt.plot(x_cors,y_cors,'b.--',ms='10')
    plt.plot(x_cors[0], y_cors[0],'rv', ms='15')
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    swipe_time = combo[0][5]
    for i in range(0,len(trail_arr)):
        if (swipe_time > time_sequence[i]) and (swipe_time <= time_sequence[i+1]):
            #time_lag = (swipe_time - time_sequence[i])/(time_sequence[i+1] - time_sequence[i])
            x_swipe = x_cors[i] #+ time_lag * (x_cors[i+1] - x_cors[i]) Different way of calculating x_swipe
            y_swipe = y_cors[i] #+ time_lag * (y_cors[i+1] - y_cors[i])
        
    plt.plot(x_swipe, y_swipe,'go',ms='15')
    plt.show()
    
    print(GESTURE_CODES_MOBILE[combo[0][3]])
    print('Change in coordinates:',(x_swipe - x_cors[0], y_swipe - y_cors[0]))




