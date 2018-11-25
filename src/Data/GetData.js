import axios from 'axios'

const GetData =  ()  =>
{ 
    var url ='http://www.ctyanalytics.com/scrapoid_answer/';

        const get_request = ()=>
        {   
            const response =   axios.get(
            url,
            {
                params : {message :'test', step :'url',url:'url'}
            }
            ).then( ()=> { return response});

        
            
            
        }
   return get_request();
}


export default GetData;