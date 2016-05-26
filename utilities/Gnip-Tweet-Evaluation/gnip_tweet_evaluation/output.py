import sys
import logging
import json
import os
import datetime
from collections import defaultdict
from math import ceil
from matplotlib import use
use('Agg')
import matplotlib.pyplot as plt
from matplotlib import dates, use
import audience_api

logger = logging.getLogger('output')

def dump_conversation(results, data_loc):
    uid = results['unique_id']
    try:
        os.stat(data_loc + uid)
    except:
        os.makedirs(data_loc + uid)

    print '\nTop Tweet terms'
    sys.stdout.write(results['body_term_count'].get_repr(10))
    top_tweet_terms_file = open(data_loc + uid + '/' + uid + '_top_tweet_terms.txt', 'w')
    top_terms = results['body_term_count'].get_repr()
    top_tweet_terms_file.write(top_terms.encode('utf-8'))
    top_tweet_terms_file.close()
    if 'RT_of_user' in results:
        RT_users = sorted(results['RT_of_user'].items(), key=lambda x: x[1][0], reverse=True)
        print '\nnumber of retweets, user id, username(s)'
        rt_users_file = open(data_loc + uid + '/' + uid + '_retweeted_users.txt', 'w')
        rt_users_file.write('number of retweets, user id, username(s)\n')
        for i, RT_user in enumerate([ str(x[1][0]) + ', ' + x[0] + ' ,' + ' ,'.join([ str(y) for y in list(x[1][1]) ]) for x in RT_users ]):
            if i <= 10:
                print RT_user
                rt_users_file.write(RT_user + '\n')
            else:
                rt_users_file.write(RT_user + '\n')

        rt_users_file.close()
    at_users = sorted(results['at_mentions'].items(), key=lambda x: x[1][0], reverse=True)
    print '\nnumber of times mentioned, user ids, username(s)'
    at_users_file = open(data_loc + uid + '/' + uid + '_at_mentioned_users.txt', 'w')
    at_users_file.write('number of times mentioned, user ids, username(s)\n')
    for i, at_user in enumerate([ str(x[1][0]) + ', ' + x[0] + ',' + ' ,'.join([ str(y) for y in list(x[1][1]) ]) for x in at_users ]):
        if i <= 10:
            print at_user
            at_users_file.write(at_user + '\n')
        else:
            at_users_file.write(at_user + '\n')

    at_users_file.close()
    if 'in_reply_to' in results:
        replied_tos = sorted(results['in_reply_to'].items(), key=lambda x: x[1], reverse=True)
        print '\nnumber of times replied to, username'
        replied_file = open(data_loc + uid + '/' + uid + '_replied_to_users.txt', 'w')
        replied_file.write('number of times replied to, username\n')
        for i, replied_to in enumerate([ str(x[1]) + ', ' + x[0] for x in replied_tos ]):
            if i <= 10:
                print replied_to
                replied_file.write(replied_to + '\n')
            else:
                replied_file.write(replied_to + '\n')

        replied_file.close()
    hashtags = sorted(results['hashtags'].items(), key=lambda x: x[1], reverse=True)
    print '\nnumber of times tweeted, hashtag'
    hashtag_file = open(data_loc + uid + '/' + uid + '_hashtags.txt', 'w')
    hashtag_file.write('number of times tweeted, hashtag\n')
    for i, hashtag in enumerate([ str(x[1]) + ', ' + x[0] for x in hashtags ]):
        if i <= 10:
            print hashtag
            hashtag_file.write(hashtag.encode('utf-8') + '\n')
        else:
            hashtag_file.write(hashtag.encode('utf-8') + '\n')

    hashtag_file.close()
    minute = results['local_timeline'].items()
    hour_dict = defaultdict(int)
    for key, value in results['local_timeline'].items():
        hour_dict[key.split(':')[0]] += value

    hour = hour_dict.items()
    times_values = sorted([ (datetime.datetime.strptime(x[0], '%H'), x[1]) for x in hour ], key=lambda x: x[0])
    times = [ x[0] for x in times_values ]
    values = [ x[1] for x in times_values ]
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 4))
    ax.plot(times, values)
    ax.set_xlabel("Users' local time", size=14)
    ax.set_ylabel('Tweets per hour', size=16)
    ax.set_title('When users Tweet during the day (based on local time)', size=14)
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    fig.autofmt_xdate()
    fig.savefig(data_loc + uid + '/' + uid + '_hourly_timeline.png')
    urls = sorted(results['urls'].items(), key=lambda x: x[1], reverse=True)
    print '\nnumber of times tweeted, base_url'
    url_file = open(data_loc + uid + '/' + uid + '_urls.txt', 'w')
    url_file.write('number of times tweeted, urls\n')
    for i, url in enumerate([ str(x[1]) + ', ' + x[0] for x in urls ]):
        if i <= 10:
            print url
            url_file.write(url.encode('utf-8') + '\n')
        else:
            url_file.write(url.encode('utf-8') + '\n')

    url_file.close()
    user_ids = sorted(results['user_ids_user_freq'].items(), key=lambda x: x[1], reverse=True)
    print '\nnumber of times tweeting, user_id'
    user_ids_file = open(data_loc + uid + '/' + uid + '_uids.txt', 'w')
    user_ids_file.write('number of times tweeting, user_id\n')
    for i, user_id in enumerate([ str(x[1]) + ', ' + x[0] for x in user_ids ]):
        if i <= 10:
            print user_id
            user_ids_file.write(user_id + '\n')
        else:
            user_ids_file.write(user_id + '\n')

    user_ids_file.close()


def dump_audience(results,data_loc):
    uid = results['unique_id']
    try:
        os.stat(data_loc + uid)
    except:
        os.makedirs(data_loc + uid)

    if 'bio_term_count' in results:
        print '\nTop bio terms (bios uniqued on user)'
        sys.stdout.write(results['bio_term_count'].get_repr(10))
        top_bio_terms_file = open(data_loc + uid + '/' + uid + '_top_bio_terms.txt', 'w')
        top_bio_terms_file.write(results['bio_term_count'].get_repr().encode('utf-8'))
        top_bio_terms_file.close()
    
    print '\nAudience API Results'
    audience_api_file = open(data_loc + uid + '/' + uid + '_audience_api.txt','w')
    if 'error' not in results['audience_api']:
        for i, (grouping_name, grouping_result) in enumerate(results['audience_api'].items()):
            print '\n' + grouping_name + '\n' + '-' * len(grouping_name)
            audience_api_file.write('\n' + grouping_name + '\n' + '-' * len(grouping_name))
            
            if 'errors' in grouping_result:
                print( grouping_result['errors'][0] )
                audience_api_file.write(grouping_result['errors'][0])
            else:
                def expand(key, value):
                    if isinstance(value, dict):
                        return [ (key + ' | ' + k, v) for k, v in flatten_dict(value).items() ]
                    elif isinstance(value, list):
                        return [] 
                    else:
                        return [(key, value)]

                flattened_result = dict([ item for k, v in grouping_result.items() for item in expand(k, v) ])
                flattened_tuples = flattened_result.items()
                grouping_result_csv = sorted(flattened_tuples, key=lambda x: (x[0].split('|')[0], -1 * float(x[-1])))
                
                for line in grouping_result_csv:
                    print line[0] + ' | ' + str(line[1]) 
                    audience_api_file.write(line[0] + ' | ' + str(line[1]) )
    else:
        print 'Error: ' + results['audience_api']['error']
        audience_api_file.write('Error: ' + results['audience_api']['error'])
    
    
    if 'age_and_gender_breakdown' in results:
        print '\nnumber of users, gender, age'
        genders = defaultdict(int)
        ages = defaultdict(int)
        for key, value in results['age_and_gender_breakdown'].items():
            genders[key[0]] += value
            ages[key[1]] += value

        total_ages_and_genders = results['age_and_gender_breakdown'].items()
        total_ages_and_genders.extend([ (('ALL_GENDERS', x[0]), x[1]) for x in ages.items() ])
        total_ages_and_genders.extend([ ((x[0], 'ALL_AGES'), x[1]) for x in genders.items() ])
        age_gen_file = open(data_loc + uid + '/' + uid + '_ages_and_genders.txt', 'w')
        for i in sorted(total_ages_and_genders):
            print i[0][0] + ',' + i[0][1] + ',' + str(i[1])
            age_gen_file.write(i[0][0] + ',' + i[0][1] + ',' + str(i[1]) + '\n')

        age_gen_file.close()
    if 'profile_locations_regions' in results:
        locs = sorted(results['profile_locations_regions'].items(), key=lambda x: x[1], reverse=True)
        print '\nnumber of occurences, country, region'
        loc_file = open(data_loc + uid + '/' + uid + '_profile_locations.txt', 'w')
        loc_file.write('number of occurences, country, region\n')
        for i, loc in enumerate([ str(x[1]) + ', ' + x[0] for x in locs ]):
            if i <= 10:
                print loc
                loc_file.write(loc.encode('utf-8') + '\n')
            else:
                loc_file.write(loc.encode('utf-8') + '\n')

        loc_file.close()

