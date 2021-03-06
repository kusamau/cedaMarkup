import math
from ceda_markup.atom.link import REL_SEARCH, REL_SELF, REL_ALTERNATE
from ceda_markup import get_mimetype
from ceda_markup.atom.atom import ATOM_LINK_REL_SEARCH, createLink

def assign_prefix(root, param):
    if param.namespace is None or param.namespace == root.attrib['xmlns']:
        return param.term_name
    
    for key, value in root.items():
        if value == param.namespace:
            return ("%s:%s") % (key[6:], param.term_name)
    
    index = 0
    while True:
        if "xmlns:a%d" % (index) not in root.keys():                
            break 
        index = index + 1
        
    root.set("xmlns:a%d" % (index), param.namespace)
    return ("a%d:%s") % (index, param.term_name)

def create_template_query(root, query):
    '''
        Creates a string to be used as parameters template list in the "description".
        As this description is used in a OpenSearch URL tag, the root parameter is required 
        in order to update the tag with the necessary namespaces
        @param root: the OpenSearchRequest.ROOT_TAG tag.
        @param query: an OSQuery instance.        
        @return: a string describing the parameters query
    '''
    template_query = ""
    for param in query.params_model:
        term = assign_prefix(root, param)
        
        url_param = ""
        if param.required:             
            url_param = ("%s={%s}") % (param.par_name, term)
        else:
            url_param = ("%s={%s?}") % (param.par_name, term)
           
        template_query += ("%s&") % (url_param)
    return template_query

COUNT_DEFAULT = 10
START_INDEX_DEFAULT = 1
START_PAGE_DEFAULT = 1

def filter_results(results, count = COUNT_DEFAULT, \
                   start_index = START_INDEX_DEFAULT, \
                   start_page = START_PAGE_DEFAULT):
    """
        Returns the opensearch results list according to the 
        'count', 'startIndex', 'startPage' parameters
        @param results: an instance or a list of instances to be displayed in 
                        the opensearch response
        @param count: the number of search results per page desired by 
                        the search client
        @param start_index: the index of the first search result desired 
                        by the search client
        @param startPage: the page number of the set of search results 
                        desired by the search client
        @return: the selected results or None if the results is None 
                        or is not a list or is an empty list
    """
    if results is None:
        return []
    elif isinstance(results, list) and len(results) == 0:
        return []
    elif not isinstance(results, list):
        _results = [results]
    else:
        _results = results
        
    tot_res = len(_results)
        
    if count is not None and count > 0:
        int_count = count
    else:
        int_count = COUNT_DEFAULT

    if start_index is not None and start_index > 1 and start_index <= tot_res:
        int_start_index = start_index
    else:
        int_start_index = START_INDEX_DEFAULT    
    
    if start_page is not None \
            and math.ceil((tot_res - int_start_index + 1)/float(int_count)) \
            >= start_page:
        int_start_page = start_page
    else:
        int_start_page = START_PAGE_DEFAULT
            
    first_result = int_start_index - 1
    last_result = first_result + int_count
    
    if int_start_page > 1 \
            and first_result + (int_start_page - 1)*int_count <= tot_res:
        first_result = first_result + (int_start_page - 1)*int_count
        
    if first_result + int_count <= tot_res:            
        last_result = first_result + int_count
    else:
        last_result = tot_res

    return _results[first_result:last_result]

def generate_autodiscovery_path(path, extension, \
                                params_model, context, \
                                rel = REL_SELF, start_index = None):
    """
        Assemble a path pointing to an opensearch engine 
        @param path: the host URL
        @param extension: the extension
        @param params_model: a list of OSParam instances
        @param context: a dictionary containing one value or None to pair with the params_model        
        @param rel: a Link type identificator. If None returns a generic ID
        @param startIndex:              
    """
    if rel == None:        
        return path

    if rel == REL_SEARCH:
        return "%s/description" % (path)
    
    if rel == REL_ALTERNATE:
        return "%s/%s" % (path, extension)

    ret = "%s/%s/?" % (path, extension)
     
    for param in params_model:
        if param.par_name == 'startIndex':
            if start_index is None:
                ret = ret + "&%s=%s" % (param.par_name, context[param.par_name])
            else:
                ret = ret + "&%s=%s" % (param.par_name, start_index)
        else:
            if param.par_name in context \
                    and context[param.par_name] is not None:
                ret = ret + "&%s=%s" \
                    % (param.par_name, context[param.par_name])                
    return ret


def create_autodiscovery_link(root, path, \
                              params_model, context, \
                              extension = None, \
                              rel = REL_SELF,
                              start_index = None):
    """
        Appends an autodiscovery link to the given 'root' document 
        @param path: the host URL        
        @param extension: the extension        
        @param rel: a Link type identificator. If None returns a generic ID
        @param params_model: a list of OSParam instances
        @param context: a dictionary containing one value or None to pair with the params_model                
    """
    href = generate_autodiscovery_path(path, extension, \
                                       params_model, context, \
                                       rel, start_index)    
    itype = get_mimetype(extension)
    if rel == ATOM_LINK_REL_SEARCH:
        itype = get_mimetype('opensearchdescription')      
    return createLink(href, rel, itype, root)                    
