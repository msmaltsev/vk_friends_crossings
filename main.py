# !usr/env/bin python3
# -*- coding: utf8 -*-

import time
from vkApiAccess import *
import json


def pairsFromList(l):
    result = []
    for i in l:
        for k in l:
            if i != k and [k, i] not in result:
                result.append([i, k])
    return result



def crossings(vk_data):
    d = {}
    people = list(vk_data.keys())
    # pairs = pairsFromList(people)
    # for p in pairs:
    #     friends_a = set(vk_data[p[0]])
    #     friends_b = set(vk_data[p[1]])
    #     intsc = friends_a & friends_b
    #     intsc_list = list(intsc)
    #     intsc_list_url = ['%s%s'%('https://vk.com/id', i) for i in intsc_list]
    #     d['%s%s|%s%s'%('https://vk.com/id', p[0], 'https://vk.com/id', p[1])] = ', '.join(intsc_list_url)
    nul = set(vk_data[people[0]])
    # print(people[0])
    # print(nul)
    for p in range(1, len(people)-1):
        set_ = set(vk_data[people[p]])
        nul = nul & set_

    d['intsc'] = nul
    
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

    # print(vk_data)

    cr = crossings(vk_data)
    # vk_data_nums = {}
    # for cr_k in cr.keys():
    #     num_key = index_userid[cr_k]
    #     cr_val_nums = [index_userid[i] for i in cr[cr_k]]
    #     vk_data_nums[num_key] = ', '.join(sorted(cr_val_nums, key = lambda x: int(x)))

    print('CROSSINGS: ', cr)
    print('FRIENDS_COUNT: ', friends_count)
    
    cr_f = open('crossings', 'w', encoding='utf8')
    # fr_f = open('friends', 'w', encoding='utf8')

    # dnums = sorted(list(init_dict.values()), key = lambda x: int(x))
    # for i in dnums:
    #     try:
    #         cr_v = vk_data_nums[i]
    #     except Exception as e:
    #         cr_v = ''

    #     try:
    #         fr_v = friends_count[i]
    #     except Exception as e:
    #         fr_v = ''

        # cr_f.write('%s\t%s\n'%(i, cr_v))
    for k in cr.keys():
        print('%s\t%s'%(k, cr[k]), file=cr_f)
    # fr_f.write('%s\t%s\n'%(i, fr_v))

    cr_f.close()
    # fr_f.close()

if __name__ == '__main__':
    main()
    # a = [1,2,3,5,6,7]
    # print(pairsFromList(a))