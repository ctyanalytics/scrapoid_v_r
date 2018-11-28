import axios from 'axios'

const GetData =  async  (current_data)  =>
{   var response=null;
    
       
        const get_request = async  ()=>
        {   
           
         response =  await axios.get(
            current_data.url,
            {
                params : {iteration:current_data.iteration,
                          current_state:current_data.current_state,
                          short_term_memory:current_data.short_term_memory
                        }
            }
         );
         return response.data;
        }
   
   return get_request();
}


export default GetData;