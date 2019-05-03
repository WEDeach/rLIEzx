from rLIEzx import *

client = MYRZX("LOGIN DATA")

print('-----------------------')
print('名前: ', client.master['master']['roleName'])
print('等級: ', client.master['master']['level'])
print('金幣: ', client.master['master']['money'])
print('')
print('共有 %s 之魔物正在孵化中' % len(client.master['alchemyStacks']))
print('背包共有 %s 個物品' %  len(client.master['items']))
print('目前共有 %s 之魔物!' % client.master['monsters'])
print('-----------------------')

input('點擊任意鍵...')
