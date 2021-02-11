#!/usr/bin/env python
# coding: utf-8

# In[38]:


import numpy as np  
import matplotlib.pyplot as plt
import pandas as pd


# In[39]:


def author(): 
    return "zliu723" 

def gtid(): 
    return 903476881


# In[40]:


def get_spin_result(win_prob): 
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result


# In[45]:


def test_code():

    win_prob = 18/38
    np.random.seed(gtid())  
    print(get_spin_result(win_prob)) 
   
    #experiment 1-1
    BETS = 1000
    test_time = 10
    wins = np.zeros((test_time,BETS+1)) 
    
    for j in range(test_time):
        winnings = np.zeros(BETS+1)
        win_prob = 18/38

        episode_winnings = 0      
        i =0                  

        while (episode_winnings<80 and i<BETS):
            won = False           
            bet_amount = 1

            while not won: 
                won = get_spin_result(win_prob)
                i = i +1

                if won == True:
                    episode_winnings = episode_winnings + bet_amount
                    winnings[i] = episode_winnings 

                else:
                    episode_winnings = episode_winnings - bet_amount
                    winnings[i] = episode_winnings
                    bet_amount = bet_amount*2

        if episode_winnings >= 80:
            winnings[i:] = 80 

        wins[j,:] = winnings 

    print(wins)
    
    #create figure 1
    for i in range(test_time):
        plt.figure(1)
        plt.xlabel('Number of bets')
        plt.ylabel('Winning amount $')
        plt.xlim(0,300)
        plt.ylim(-256,100)
        plt.title('Figure 1 - 10 simulations result')
        plt.plot(pd.Series(wins[i]))
        plt.savefig('Figure 1.png')   
        
    #experiment 1-2
    BETS = 1000
    test_time = 1000
    wins = np.zeros((test_time,BETS+1)) 


    for j in range(test_time):
        winnings = np.zeros(BETS+1)
        win_prob = 18/38

        episode_winnings = 0       
        i =0                       

        while (episode_winnings<80 and i<BETS):
            won = False           
            bet_amount = 1

            while not won: 
                won = get_spin_result(win_prob)
                i = i +1

                if won == True:
                    episode_winnings = episode_winnings + bet_amount
                    winnings[i] = episode_winnings 

                else:
                    episode_winnings = episode_winnings - bet_amount
                    winnings[i] = episode_winnings
                    bet_amount = bet_amount*2

        if episode_winnings >= 80:
            winnings[i:] = 80
        wins[j,:] = winnings
    
    mean_wins=np.mean(wins,axis=0)
    std_wins=np.std(wins,axis=0)
    median_wins=np.median(wins,axis =0)
    
    #create figure 2
    upper_mean = mean_wins+std_wins
    lower_mean = mean_wins-std_wins

    
    plt.figure(2)
    plt.xlabel('Number of bets')
    plt.ylabel('Winning amount $')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.title('Figure 2 - 1000 simulations for mean and std')

    plt.plot(range(300),mean_wins[:300], color='r',label = 'mean')
    plt.plot(range(300),upper_mean[:300], color='b',label = 'mean + std')
    plt.plot(range(300),lower_mean[:300], color='g',label = 'mean - std')
    plt.legend(framealpha=1, frameon=True)


    plt.savefig('Figure 2.png')
        
    #create figure 3
    upper_median = median_wins+std_wins
    lower_median = median_wins-std_wins

    
    plt.figure(3)
    plt.xlabel('Number of bets')
    plt.ylabel('Winning amount $')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.title('Figure 3 - 1000 simulations for median and std')

    plt.plot(range(300),median_wins[:300],label = 'median')
    plt.plot(range(300),upper_median[:300],label = 'median + std')
    plt.plot(range(300),lower_median[:300],label = 'median - std')
    plt.legend(framealpha=1, frameon=True)
    plt.savefig('Figure 3.png')
        
    #experiment 2
    
    BETS = 1000
    test_time = 1000
    wins = np.zeros((test_time,BETS+1))
    
    for j in range(test_time):
        winnings = np.zeros(BETS+1)
        win_prob = 18/38
        episode_winnings = 0       
        i =0   
        while episode_winnings<80 and i< BETS and episode_winnings>-256:
            won = False           
            bet_amount = 1

            while (not won) and (i < BETS):
                won = get_spin_result(win_prob)
                i = i +1

                if won == True:
                    episode_winnings = episode_winnings + bet_amount
                    winnings[i] = episode_winnings 

                else:
                    episode_winnings = episode_winnings - bet_amount
                    winnings[i] = episode_winnings

                    if (bet_amount >=episode_winnings + 256):
                        bet_amount = episode_winnings + 256
                    else:
                        bet_amount = bet_amount*2

        if episode_winnings >= 80:
            winnings[i:] = 80 
        elif episode_winnings <= -256:
            winnings[i:] = -256
        else:
            continue
            
        wins[j,:] = winnings
        
    mean_wins=np.mean(wins,axis=0)
    std_wins=np.std(wins,axis=0)
    median_wins=np.median(wins,axis =0)
    
    #create figure 4
    upper_mean = mean_wins+std_wins
    lower_mean = mean_wins-std_wins

    
    plt.figure(4)
    plt.xlabel('Number of bets')
    plt.ylabel('Winning amount $')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.title('Figure 4 - 1000 simulations for mean and std')

    plt.plot(range(300),mean_wins[:300], color='r',label = 'mean')
    plt.plot(range(300),upper_mean[:300], color='b',label = 'mean + std')
    plt.plot(range(300),lower_mean[:300], color='g', label = 'mean - std')
    plt.legend(framealpha=1, frameon=True)
    plt.savefig('Figure 4.png')
    
    #create figure 5
    upper_median = median_wins+std_wins
    lower_median = median_wins-std_wins

    
    plt.figure(0)
    plt.xlabel('Number of bets')
    plt.ylabel('Winning amount $')
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.title('Figure 5 - 1000 simulations for median and std')

    plt.plot(range(300),median_wins[:300],label = 'median')
    plt.plot(range(300),upper_median[:300], label = 'median + std')
    plt.plot(range(300),lower_median[:300], label = 'meidna - std')
    plt.legend(framealpha=1, frameon=True)
    plt.savefig('Figure 5.png')


# In[46]:


if __name__ == "__main__": 
    test_code()  


# In[ ]:




