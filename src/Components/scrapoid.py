#IMPORTS
#=============================================================================
import requests
import sys
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
from lxml import etree
from tools import generate_proxy
from tools import clean_css
from tools import create_folder
from flask import jsonify
import os
class scrapoid:

    target              =None
    html                =None
    url                 =None
    trials              =5
    scrapoid_memory     ={}
    memory_location     =None
    type_req            =None
    number_parameters   =0
    url_format          =None
    learned_structures={ 'tables':  { 'grouper':'table','items':'tr','items_data':'td'},
                         'lists':   {'grouper': 'body', 'items': 'ul', 'items_data': 'li'}

    }
    def __init__(self,memory_location='no_memory_location',url='no_url',proxy=False,type_req='get',url_format=None,default_param=[]):

        self.url            =url
        self.memory_location=memory_location
        self.type_req       =type_req
        self.url_format     =url_format
        print('____/SCRAPOID\__vP.1.0__')
        print("> Hello Human")
        print("> I have been created by Omar, the best creators of all (at least better than luis)")
        if url=='no_url':
            print('> No url provided, I believe I am gonna use my memory to scrap data')
        else:
            print(f'> An URL has been provided, connecting , number of trials to get the website  are {self.trials}...')

            if url_format is None:
                print('> No url format has been provided, no parameters then, scrapoid is gonna use raw url')
                if self.get_html(self.url,proxy,type_req):
                   print("> Getting the website was yummmy and .. successfull")
                else:
                    print(f"> Even after {self.trials} trials, could not get the website ... ")
            else:
                print('> A format has been provided')
                print('>'+str(url_format[0]))
                number_parameters=str(url_format[0]).count('param[')
                print('> Scrapoid had detected '+str(number_parameters)+' parameters')
                if len(default_param)==int(number_parameters):
                    print('> Number of default parameters is ok , nice !')
                else :
                    print('> Number of default parameters does not match url')

                param=default_param
                generated_url= str(url_format[1])
                print('> Generated default url is: ' +str(generated_url)+' moving forward with it')


                if self.get_html(generated_url,proxy,type_req):
                   print("> Getting the website was yummmy and .. successfull")
                else:
                    print(f"> Even after {self.trials} trials, could not get the website ... ")
    def detect_urls(self,message):
        def Find(string):
            # findall() has been used
            # with valid conditions for urls in string
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
            return url
        urls=Find(message)
        if len(urls)> 0 : return True,urls
        else : return False,None
    def jsonify_with_htmls(self,data):

         from xml.etree import ElementTree as et
         answer=[]


         for item in data:
             v=self.clean_data(item['data_dataframe'])
             v=item['data_dataframe']
             v=v.to_html(classes=["display nowrap"])
             #t = et.fromstring(v)
             #t.set('id', 'table_result')
             #v=et.tostring(t)

             k=item['data_description']
             answer.append({'data_info':k, 'data':v})

         answer=json.dumps(answer)
         answer=json.loads(answer)
         #answer=jsonify(answer)
         return answer
    def get_html(self,url,proxy=False,type_req='get'):

         if type_req=='post':

                    from pathlib import Path
                    search_request = Path(self.memory_location+'/search_request.py')
                    if search_request.is_file():
                        sys.path.append(self.memory_location)
                        import search_request as sr
                        sreq=sr.search_request
                        print('> Search request provided ... OK posting.')
                    else:
                        print('> Search request not provided it ... please provided first.')
                        return False

         trial=0
         website_found=False
         while website_found==False and trial<=self.trials:
             trial+=1
             print("> Attempt number #"+str(trial))
             try:
                 if proxy:
                     print('> Using proxy ...')
                     proxy_ip=generate_proxy()
                     if str(proxy_ip) =="0" :
                             if type_req=='get':
                                 r = requests.get(
                                    url=url)
                             else:
                                 r = requests.post(
                                    url=url,
                                    data=sreq,
                                    headers={
                                        'X-Requested-With': 'XMLHttpRequest'
                                    })

                     else:

                             proxies = {'http': 'http://'+str(proxy_ip), 'https': 'https://'+str(proxy_ip)}
                             if type_req=='get':
                                 r = requests.get(
                                    url=url,
                                   proxies=proxies
                                   )
                             else:
                                 r = requests.post(
                                    url=url,
                                    data=sreq,proxies=proxies,
                                    headers={
                                        'X-Requested-With': 'XMLHttpRequest'
                                    })
                 else:
                      print('> Not using proxy ...')
                      if type_req=='get':
                          r = requests.get(
                                    url=url)
                      else:
                          r = requests.post(
                                    url=url,
                                    data=sreq,
                                    headers={
                                        'X-Requested-With': 'XMLHttpRequest'
                                    })

                 self.html=r.text
                 website_found=True
             except Exception as exp:
                print(exp)
                website_found=False
         return website_found
    def clean_data(self,data,custom_words=[]):
        data[data.columns]=data[data.columns].applymap(lambda x : (clean_css(str(x),custom_words)))
        return data
    def search_mode(self,target='tables',debug=True,only_text=True):
          self.target=target
          print(f"> I understand you want to scrape {target} from your url, let 's go !")

          # case post works only in local scrapoid
          if self.type_req=='post':
                    data=self.detect_type_reponse(self.html)
                    self.html=data

          if target in self.learned_structures:
              print(f'> I know how to scrape  {target} !')

              data=self.listAll_v2( html=self.html, target=target,only_text=only_text,struct=None,get_data=False,filter_dimension=None)

              print('> Would you like me to memorize one of those ?')
              answer=str(input())

              if answer.upper()=='YES':
                  print('> Ok so please give me the number, follow by its module and name like this number-module-name')
                  answer = str(input())
                  answer=answer.split('-')
                  number=answer[0].replace(' ','')
                  module = answer[1].replace(' ', '')
                  name = answer[2].replace(' ', '')

                  if self.memorize_v2( number, module, name, data,only_text, recompute_location=True):
                      print('> Memorized successfully')
                  else:
                      print('> Sorry , I could not memorize it')
              else:
                  print('> I am already bored')

          else:
              print(f'> I do not know how to scrape  {target}, please give me the structure !')
    def memorization(self,data_new):
        import json
        try:
            jsonFile = open(self.memory_location+"/scrapoid_memory.json", "r+") # Open the JSON file for reading
            data = json.load(jsonFile) # Read the JSON into the buffer
            jsonFile.close() # Close the JSON file

            ## Working with buffered content
            data=dict(data)
            data.update(data_new)

                ## Save our changes to JSON file
            jsonFile = open(self.memory_location+"/scrapoid_memory.json", "w+")
            jsonFile.write(json.dumps(data))
            jsonFile.close()
        except:
          jsonFile = open(self.memory_location+"/scrapoid_memory.json", "w+")
          jsonFile.write(json.dumps(data_new))
          jsonFile.close()
    def go_scrape_memorized(self,name,proxy=False,param=[]):
        from distutils.util import strtobool
        status,xpath,url,cols,type_req,url_format,only_text,struct=self.remember_table(name)
        only_text=strtobool(str(only_text))
        success_status=True
        error=None
        if not status:
            success_status=False
            error="Memorization file not found"
            return pd.DataFrame(),success_status,error
        else:
            print('____/SCRAPOID\____')
            print(f'> Scrapoid has searched with a status  {status}')
            print(f'> Scrapoid has searched with xpath  {xpath}')
            print(f'> Scrapoid has searched with a url  {url}')
            print(f'> Scrapoid has searched with a type_req  {type_req}')
            print(f'> Scrapoid has searched with a url_format  {url_format}')
            print('__________________')

            if struct is not None:
                grouper = struct['grouper']
                items = struct['items']
                items_data = struct['items_data']
            else:
                    success_status=False
                    error="Struct not found"
                    print(error)
                    return pd.DataFrame(),success_status,error

            #so far so good getting website content
            try:
                if self.type_req=='get':

                    if url_format is not None:
                        url=url_format.format(**locals())
                    else:
                        pass
                    print(url)
                    self.get_html(url,proxy,type_req)
                    data=self.html
                elif self.type_req=='post':
                        self.get_html(url,proxy,type_req)
                        data=self.detect_type_reponse(self.html)
            except Exception as excp:
                    success_status=False
                    error="Error while getting website content : "+str(excp)
                    print(error)
                    return pd.DataFrame(),success_status,error

            #so far so good, processing html with the tree
            try:
                    tree = etree.HTML(data)
                    list_table_global=[]


                    #check if headers exists for columns:
                    headers = tree.xpath(xpath+'//th')
                    dict_header={}
                    iterator_header=0

                    for elem_header in headers :
                        th_data=BeautifulSoup(etree.tostring(elem_header),"lxml").find('th')
                        dict_header[iterator_header]=th_data.text
                        iterator_header+=1
                    if len(headers)>0:
                        list_table_global.append(dict_header)

                    r_rows = tree.xpath(xpath+'//'+items)
                    number_rows=len(r_rows)

                    for elem_table in r_rows:

                        r_data = tree.xpath(elem_table.getroottree().getpath(elem_table)+'//'+items_data)
                        iterator=0
                        dict_table={}
                        for data in r_data:



                            td_data=BeautifulSoup(etree.tostring(data),"lxml").find(items_data)
                            if only_text :
                                text_data = td_data.text
                            else:
                                text_data=td_data.contents

                            dict_table[iterator]=text_data
                            iterator+=1
                            if iterator%cols==0 and iterator >0:
                                list_table_global.append(dict_table)
                                iterator=0
            except Exception as excp:
                    success_status=False
                    error="Error while processing html : "+str(excp)
                    print(error)
                    return pd.DataFrame(),success_status,error

        print('> Data retrieved successfully, parsing it to Dataframe, see ya !')
        r_data.clear()
        r_rows.clear()
        headers.clear()
        tree.clear()
        return pd.DataFrame(list_table_global),success_status,error
    def memory(self):
        import json

        with open(self.memory_location+"/scrapoid_memory.json", 'r') as data:
          data=json.load(data)
        print(data)
    def remember_table(self,name):
        import json

        with open(self.memory_location+"/scrapoid_memory.json", 'r') as data:
          data=json.load(data)
        memory=(dict(data))
        xpath=None
        url=None
        cols=None
        type_req=None
        url_format=None
        found=False
        only_text=None
        struct=None
        for k,v in memory.items():
            try:
               if k==name+'_xpath':
                 xpath=v
                 found=True
               elif k==name+'_url':
                  url=v
                  found=True
               elif k==name+'_columns':
                  cols=v
                  found=True
               elif k==name+'_req_type':
                  type_req=v
                  found=True
               elif k==name+'_url_format':
                  url_format=v
                  found=True
               elif k == name + '_only_text':
                   only_text = v
                   found = True
               elif k == name + '_struct':
                   struct = v
                   found = True
            except Exception as ex:
                print(ex)


        return found,xpath,url,cols,type_req,url_format,only_text,struct
    def find_values(self,target, obj):
        result=[]

        def _find_values(target,obj):

            if type(obj) == list:
                i=0
                for elem in obj:
                    _find_values(target,elem)
                    i+=1
            elif type(obj) == dict:
                for k_elem,v_elem in obj.items():
                    _find_values(target,v_elem)

            else:
                try:
                    if target in obj:
                        print('> Scrapoid algorithm found a table in your json')
                        result.append(obj)


                except:
                    pass
        _find_values(target,obj)
        return result
    def detect_type_reponse(self,res):
        print('> Scrapoid analysing the reponse')
        try:
          data = json.loads(res)


          print('> Your data is a json bro ! looking for target element ')


          data = self.find_values("<table",data)

          #assumption that answer to post request yields only to one table
          data=data[0]
          return data
        except Exception as exc:
            print(exc)
    def listAll_v2(self,html,target,only_text=True,struct=None,get_data=False,filter_dimension=None):
        # 3 levels structure

        grouper=None #aggregate element , could be  table 'table'
        items=None # distinctive element, coulb be rows 'tr'
        items_data=None # distinctive element data, coulb be 'td'

        if struct is not None :
              grouper=struct['grouper']
              items=struct['items']
              items_data=struct['items_data']
        else:
            struct={}
            try:
              struct['grouper']=self.learned_structures[target]['grouper']
              struct['items']=self.learned_structures[target]['items']
              struct['items_data']=self.learned_structures[target]['items_data']
              grouper=struct['grouper']
              items=struct['items']
              items_data=struct['items_data']
            except:
                print('Structure of '+target+' unknown, please provide one')

        #text of the answer init
        text_answer=""

        #in case of getting data activated:
        # in other words: list of dataframes
        listAll_global=[]
        data_descr=None
        #init of the tree element
        tree = etree.HTML(html)

        print(struct)
        print("""\n> Scrapoid looking ...""")
        #looking
        g = tree.xpath(f"//{grouper}")
        grouper_len=len(g)


        print(f"""\n> Scrapoid has found {grouper_len} {grouper}(s)""")
        grouper_iterator=0
        for aggregate in g:
            aggregate_datas=[]

            grouper_iterator+=1

            #getting information on each item
            #----------------------------------

            #xpath of the item
            xpath=aggregate.getroottree().getpath(aggregate)
            xpath_location_memorized=xpath

            #going down to level 2
            items_aggregated = tree.xpath(xpath+f'//{items}')
            items_aggregated_len=len(items_aggregated)

            #check if headers exists for columns:
            headers = tree.xpath(xpath+'//th')
            dict_header={}
            iterator_header=0

            for elem_header in headers :
                   th_data=BeautifulSoup(etree.tostring(elem_header),"lxml").find('th')
                   dict_header[iterator_header]=th_data.text
                   iterator_header+=1
            if len(headers)>0:
                aggregate_datas.append(dict_header)

            #going down to level 3
            for item in items_aggregated:
                  #xpath of the item
                    xpath=item.getroottree().getpath(item)
                   #going down to level 2
                    item_data_all = tree.xpath(xpath+f'//{items_data}')
                    item_data_len=len(item_data_all)
                    aggregate_data={}
                    iterator_data=0
                    #we assume data is uniformat



                    for data in item_data_all:
                        iterator_data+=1
                        granular_data=BeautifulSoup(etree.tostring(data),"lxml").find(items_data)
                        if only_text :
                            granular_data_as_text = granular_data.text
                        else:
                            granular_data_as_text = granular_data
                        aggregate_data[iterator_data]=granular_data_as_text
                    if filter_dimension is not None :
                        if     int(item_data_len)==int(filter_dimension) :
                            aggregate_datas.append(aggregate_data)
                    else:
                             aggregate_datas.append(aggregate_data)


            text_answer+=f"""\n> --------------------------------------"""
            text_answer+=f"""\n> {grouper} #{grouper_iterator} with more than :{items_aggregated_len} aggregated element(s) and {item_data_len} dimension(s)"""
            data_descr=f"""#{grouper_iterator} {grouper} with more than :{items_aggregated_len} aggregated element(s) and {item_data_len} dimension(s)"""
            data_descr+=f""" located in :{xpath_location_memorized}"""

            data_info={'target': grouper,'number': grouper_iterator,'dimension': item_data_len,  'xpath': xpath_location_memorized, 'struct': struct
            }




            if  item_data_len > 0 :
                data={}
                data['data_info']=data_info
                data['data_description']=data_descr
                data['data_dataframe']=pd.DataFrame(aggregate_datas)
                listAll_global.append(data)
        print(text_answer)
        if get_data:
            for dataframe in listAll_global:
                print(dataframe.head(10))
        print(listAll_global)
        return listAll_global
    def process_web_message(self,url,step,message):
      try:
        if step=='url':
            if str(message).replace(" ","") != ""   :
                url=message
                answer="Yum ... yum, the website is in my belly now hehe. Tell me, What do you need ?"
                return answer
        if step=='ask_element':

                answer=f"... Ok i will get you your {message}"
                data=self.listAll_v2(self.html,message)
                answer=self.jsonify_with_htmls(data)

                return answer
        if step=='memorize_element':

            import json

            info_memorization=json.loads(message)
            data=self.listAll_v2(self.html,'tables')

            number=info_memorization['number']
            module = info_memorization['module']
            name =info_memorization['name']

            if self.memorize_v2( number, module, name, data,True, recompute_location=True):
                      return  '  Yo, I have memorize it sucessfully  ! need anything else ?'
            else:
                      return 'Oups, I failed ...'
        if step == 'memorization':
            if message=='yes':
                answer = " Alright ! Please give me its number followed by its module and the name you want to give to this task as format : number-module-script"
            else:
                answer =' I am bored ..'
            return answer
        return "euh .. what ? "
      except Exception as excep:
          return 'Yo, an error occured ...'+str(excep)+' Please check with my creator ! write "reset" to reset me'
    def memorize_v2(self,number_table,module,name,result_find_all,only_text,recompute_location=True):

      try:
            self.scrapoid_memory=dict()
            dict_info={}
            dict_info['module']=module
            dict_info['name']=name
            for data in result_find_all:
                 if (int(data['data_info']['number'])==int(number_table)):

                        dict_info['xpath']=data['data_info']['xpath']
                        dict_info['dimension']=data['data_info']['dimension']
                        dict_info['struct']=data['data_info']['struct']
                        dict_info['target']=data['data_info']['target']
                        break



            module=dict_info['module']
            #check existence otherwise create it and modify self
            if recompute_location:
                memory_path=os.getenv("HOME") + "/github/CtyAnalytics_dcore/routines/"+module+"/component"
                template_script=os.getenv("HOME") + "/github/CtyAnalytics_dcore/routines/TEMPLATE_MODULE/scrapper_algorithm.py"
                script_path=os.getenv("HOME") + "/github/CtyAnalytics_dcore/routines/"+module
                create_folder(memory_path)
                self.memory_location=memory_path
                from shutil import copy
                try:
                 copy(template_script, script_path)

                except:
                    pass
            name=dict_info['name']
            self.scrapoid_memory[name+'_xpath']=dict_info['xpath']
            self.scrapoid_memory[name+'_url']=self.url
            self.scrapoid_memory[name+'_only_text']=only_text
            self.scrapoid_memory[name+'_struct']=dict_info['struct']
            self.scrapoid_memory[name+'_target']=dict_info['target']
            if self.url_format is not None:
                self.scrapoid_memory[name+'_url_format']=self.url_format[0]
            self.scrapoid_memory[name+'_columns']=dict_info['dimension']
            self.scrapoid_memory[name+'_req_type']=self.type_req
            self.memorization(self.scrapoid_memory)
            return True
      except Exception as ex:
          print('Error '+ex)
          return False
    def process_web_message_vReact(self,iteration,current_state,short_term_memory):
        # TODO in front end side
        #________________________
        short_term_memory = json.loads(short_term_memory)


        #State Transition Matrices
        states = [ {"i":0, "state":"null","type_card":"null"} ,
                   {"i":1, "state":"Let's get started","type_card":"intro"},
                   {"i":2, "state":"any input","type_card":"input"},
                   {"i":3, "state":"Tables","type_card":"discussion"}
                        ]
        transitions = [ {"i":1, "props" : { "type_card":"intro", "text":"Hello I am scrapoid, I can scrap websites for you !", "choices":["Let's get started"]}} ,
                      {"i":2, "props" : { "type_card":"input", "text":"Can you give me the url please "}},
                       {"i":3,
                       "props" : { "type_card":"discussion", "text":"What do you need ? ","choices":["Tables","Lists"], "memorize":"url"}
                       },
                       {"i":4,
                       "props" : { "type_card":"show", "text":"<answer>","choices":["<choice>"], "memorize":"choice","memorize_data":"<data>"}
                       }

                ]

        next_iteration="null"
        next_props="null"

        for j in range(len(states)) :

                   if ((states[j]["i"]==iteration)
                 and (
                     (states[j]["state"]==current_state) and (states[j]["type_card"] !="input")
                        or (states[j]["type_card"] =="input")
                        or ((states[j]["state"]==current_state) and (states[j]["type_card"] !="intro"))
                        )
                 ) :





                                    if (iteration==3):
                                        # found content case

                                            if self.get_html(short_term_memory["url"],False,'get'):
                                                 data=self.listAll_v2(self.html,current_state.lower())
                                                 answer=self.jsonify_with_htmls(data)

                                                 transitions[j]["props"]["data"]=answer
                                                 transitions[j]["props"]["choices"]=[str(i) for i in range(len(data))]
                                                 transitions[j]["props"]["text"]="Found "+str(len(data))+" "+current_state

                                                 next_iteration=transitions[j]["i"]
                                                 next_props=transitions[j]["props"]
                                            else:
                                                print(f"> Even after {self.trials} trials, could not get the website ... ")



                                    else :

                                        next_iteration=transitions[j]["i"]
                                        next_props=transitions[j]["props"]


                                    response = {'i':next_iteration,"props":next_props}
                                    print(response)
                                    return response
        return  transitions[0]







