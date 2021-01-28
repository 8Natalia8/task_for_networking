'''
 комментарии к лучшему пониманию происходящего в программе приведены ниже
@author: nataa
'''

from ipaddress import IPv4Address, IPv4Network
import random
from pip._vendor.urllib3.packages.ssl_match_hostname._implementation import ipaddress
from scapy.volatile import RandIP
import socket
import struct

def cidr_to_netmask(mask):
    host_bits = 32 - int(mask)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return netmask

def intcaststr(bitlist):
    return int("".join(str(i) for i in bitlist), 2)

def generate(value):
    
    #выбираем рандомно маску
    masks=range(0,32,1)
    
    for i in range(value):
        #выбираем рандомно ip-адресс
        adr=ipaddress.ip_address(RandIP())
        mask_for_adr=random.choice(masks)
        #print('mask','/',mask_for_adr)
        
        #представляем маску в формате вида 255.255.255.0
        mask32=cidr_to_netmask(mask_for_adr)
        #print('mask32',mask32)
        
        #преобразуем маску в бинарный вид      
        mask_in_bit=[format(int(bits),'b') for bits in mask32.split(".")]
        for ind,i in enumerate(mask_in_bit):
            if i=='0':#надо дописать до байта,если только один ноль в октете для последующего бъединения всех 4 октетов
                mask_in_bit[ind]='00000000'

        #print(mask_in_bit)
        
        mask_buff=''.join(mask_in_bit)  #строка с 4-мя октетами в бинарном виде      
        #print('mask_buff:',mask_buff)
        
        #преобразуем строку в int
        mask_int=intcaststr(mask_buff)
       # print('mask_int',mask_int)
        
        #определяем подсеть путем побитовой конъюнкции адреса и маски
        the_subnet=int(adr) & mask_int
        #print('adr in int:',int(adr),'mask_int in int',mask_int)
        #print('subnet:',the_subnet)

        #теперь подсеть надо привести к виду объекта ipaddress.ip_network
        #print(str(the_subnet))
        subnet_good=ipaddress.ip_network(the_subnet)
        #к подсети записываем сгенерированную раннее маску
        subnet_good=IPv4Network(str(subnet_good).split('/')[0]+'/'+str(mask_for_adr))             
        #print('NORMAL LOOK',str(subnet_good))
         
        #записываем итоговый результат
        file_out=open('autogen.txt','a',encoding='utf-8')        
        file_out.write(str(subnet_good)+'\n')
        file_out.close()
    #print('Success!') 
    



#main    
file_in=open('in.txt','r')
n=int(file_in.readline())
#print(n)
add=file_in.readline().strip()
#print(type(add))
add_to_ip4=IPv4Address(add)
#print(add_to_ip4)
#print(type(add_to_ip4))
#вызов функции генерации n валидных подсетей
generate(n)
generated_subnets=[]
generated_subnets=open('autogen.txt').read().split('\n')
generated_subnets.pop(-1) #убираем последний элемент перевода строки
#print('!!!',generated_subnets)
file_out=open('out.txt','a',encoding='utf-8')

equal_masks=[] #список для возможных маршрутов 
for gen in generated_subnets:
    #print(type(gen))
    gen=IPv4Network(gen)
    #print(type(gen))
    #print(gen.prefixlen)
    if add_to_ip4 in gen:
        #print('here is')
        equal_masks.append(gen)           
    else:
        continue
    
#print(equal_masks)    
if len(equal_masks)==0:
    file_out.write('There are no subnets for this ip,the one possible is 0.0.0.0/0\n')
else:    
    #находим маску с наибольшим значением
    smallest_net=equal_masks[0]
    #print(type(smallest_net),smallest_net)                     
    for each in equal_masks:
        #print(each)
        each=IPv4Network(each)
        #print(each)
        if each.subnet_of(smallest_net):
            #print('meow',each)
            smallest_net=each 
        else:
                continue
    #print('final',smallest_net)          
    file_out.write(str(add_to_ip4)+'\n')
    file_out.write(str(smallest_net)+'\n')
    
file_out.close()
file_in.close()
    
