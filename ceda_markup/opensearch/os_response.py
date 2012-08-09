'''
BSD Licence
Copyright (c) 2012, Science & Technology Facilities Council (STFC)
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
        this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.
    * Neither the name of the Science & Technology Facilities Council (STFC) 
        nor the names of its contributors may be used to endorse or promote 
        products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, 
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on 24 May 2012

@author: Maurizio Nagni
'''
from ceda_markup.opensearch.os_request import OS_ROOT_TAG, OS_NAMESPACE,\
    OS_PREFIX
from ceda_markup.markup import createSimpleMarkup

MAX_OS_SHORT_NAME_LEN = 16
MAX_OS_LONG_NAME_LEN = 48
MAX_OS_TAGS_LEN = 256
MAX_OS_DESCRIPTION_LEN = 1024
MAX_OS_DEVELOPER_LEN = 64
MAX_OS_ATTRIBUTION_LEN = 256

SYNDACATION_OPEN = 'open'
SYNDACATION_LIMITED = 'limited'
SYNDACATION_PRIVATE = 'private'
SYNDACATION_CLOSED = 'closed'
OS_SYNDACATION_RIGHT = [SYNDACATION_OPEN, SYNDACATION_LIMITED, SYNDACATION_PRIVATE, SYNDACATION_CLOSED]
OS_SYNDACATION_RIGHT_DEFAULT = SYNDACATION_OPEN

OS_ADULT_CONTENT_DEFAULT = False
OS_INPUT_ENCODING_DEFAULT = 'UTF-8'
OS_OUTPUT_ENCODING_DEFAULT = 'UTF-8'

def createTotalResults(total_results, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):    
    tr = total_results
    if isinstance(total_results, int):
        tr = str(total_results)
    return createSimpleMarkup(tr, root, 'totalResults', ns, OS_PREFIX)

def createStartIndex(start_index, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):    
    tr = start_index
    if isinstance(start_index, int):
        tr = str(start_index)
    return createSimpleMarkup(tr, root, 'startIndex', ns, OS_PREFIX)

def createItemsPerPage(items_per_page, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):    
    tr = items_per_page
    if isinstance(items_per_page, int):
        tr = str(items_per_page)
    return createSimpleMarkup(tr, root, 'indexPerPage', ns, OS_PREFIX)

def createOpenSearchRespose(root, totalResults = None, startIndex = None, itemsPerPage = None, queries = None):                
    if totalResults is not None:
        markup = createTotalResults(totalResults, root)
        root.append(markup)            
    
    if startIndex is not None:
        markup = createStartIndex(startIndex, root)
        root.append(markup)            
                    
    if itemsPerPage is not None:
        markup = createItemsPerPage(itemsPerPage, root)
        root.append(markup)

    for query in queries:                       
        root.append(query)