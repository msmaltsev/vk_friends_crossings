# !usr/env/bin python3
# -*- coding: utf8 -*-

import time
from vkApiAccess import *
import json

def crossings(vk_data):
    d = {}
    people = vk_data.keys()
    people_set = set(people)
    for k in people:
        friends_set = set(vk_data[k])
        intsc = friends_set & people_set
        d[k] = list(intsc)
    return d


def initDict(file = 'src', n = 15):
    d = {}
    f = open(file, 'r', encoding='utf8')
    for line in f:
        line = line.strip('\n')
        num, link = line.split('\t')
        d[link[n:]] = num
    return d


def getUserIds(screennames, access_token):
    sc = ','.join(screennames)
    res = callVkApi('users.get', access_token, user_ids = sc, fields='screen_name')
    print(res)


def main():

    access_token = open('access_token', 'r', encoding='utf8').read()
    init_dict = initDict()
    # print(init_dict)

    print('retrieving user ids...')
    index_userid = {}
    allnames = list(init_dict.keys())
    for i in allnames:
        res = callVkApi('users.get', access_token, user_ids = i, fields='screen_name')
        try:
            print(i, res[0]['id'])
            index_userid[ str(res[0]['id']) ] = init_dict[i]
        except Exception as e:
            print(i, e)
        time.sleep(0.3333333)
    print('')

    friends_count = {}
    vkids = index_userid.keys()
    vk_data = {}
    for i in vkids:
        n = callVkApi('friends.get', access_token, user_id = i)
        print(i, n['count'])
        friends_count[index_userid[i]] = n['count']
        n_ids = n['items']
        s_ids = [str(i) for i in n_ids]
        vk_data[str(i)] = s_ids
        time.sleep(0.333333)
    print('')

    cr = crossings(vk_data)
    vk_data_nums = {}
    for cr_k in cr.keys():
        num_key = index_userid[cr_k]
        cr_val_nums = [index_userid[i] for i in cr[cr_k]]
        vk_data_nums[num_key] = ', '.join(sorted(cr_val_nums, key = lambda x: int(x)))

    print('CROSSINGS: ', vk_data_nums)
    print('FRIENDS_COUNT: ', friends_count)
    
    cr_f = open('crossings', 'w', encoding='utf8')
    fr_f = open('friends', 'w', encoding='utf8')

    dnums = sorted(list(init_dict.values()), key = lambda x: int(x))
    for i in dnums:
        try:
            cr_v = vk_data_nums[i]
        except Exception as e:
            cr_v = ''

        try:
            fr_v = friends_count[i]
        except Exception as e:
            fr_v = ''

        cr_f.write('%s\t%s\n'%(i, cr_v))
        fr_f.write('%s\t%s\n'%(i, fr_v))

    cr_f.close()
    fr_f.close()

if __name__ == '__main__':
    main()