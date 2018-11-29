<head>
    <title>Keyword search enginee</title>
</head>
<style>
	th {
	    text-align: left;
	    padding: 8px;
	}
	
	ul {
	  list-style-type: none;
	}
	
	ul li{
		display:inline;
	}
</style>
<body>
% if user_email:
	<form action="/logout" method="post">
        <input value="Sign out" type="submit" style="float:right;margin-left:0.5em"/>
    </form>
	<span style="float:right;">Welcome, {{user_email}}</span>
	<br>

% else:
	<form action="/login_step1" method="post">
        <input value="Sign in" type="submit" style="float:right;margin-left:0.5em"/>
    </form>
	<span style="float:right;">Welcome, anonymous</span>
	<br>
	
% end
    <div><h1 style="text-align:center;">NEET SEARCH ENGINEE</h1> 
	<div><image src="/static/xiaomai.jpeg" style="width:10%;margin:auto;display:block"/></div>
	<form action="/" method="post">
    	<div style="text-align:center">Please enter the keywords: <input name="keywords" type="text" />
        <input value="search" type="submit" />
		</div>
    </form>
	
<!--show the results if keywords entered -->
% if keywords: 
%	word = keywords.lower().split()[0]
	<h1 align="center">Search for "{{word}}"</h1>

<!--count is a dict storing each keyword and its number of occurence, it is used in result table-->
<!--temp dict is used in the case where there are already 20 keywords stored in the record dict, those new keywords are temporarily stored in temp and will be used to compare with the current top 20 popular keywords. Keywords having larger number of occurence will be put or remained in record dict-->
<%
	count = {}  
	
	if word not in count:
		count[word]=1
	else:
		count[word]+=1
	end
		
	if user_email:
		if word not in record:
			if len(record) < 10:
				record[word]=1
			else: 
				record.popitem(last=False)	
				record[word]=1			
			end
		else:
			temp = record[word]
			del record[word]
			record[word]= temp+1
		end
	end

%>
<% if word in resolved_inverted_index:
      urls = resolved_inverted_index[word]
	  ranked_url = {}
	  for url in urls:
	  	 url_id = lexicon[url]
		 url_score = page_rank[str(url_id)]
		 ranked_url[url_score] = url
	  end
	  
	  ranked_url = sorted(ranked_url.iteritems())	
	  num_of_page = len(ranked_url)/5+1     
	  curr_page = int(page_num)
%>
	<table id=”results” style="margin:auto">
		<tr style="font-size:1.5em">
			<th>Rank</th>
			<th>Urls</th>
		</tr>
<%
	start_index = 5*(curr_page-1)
	end_index = 5*curr_page
	counter = start_index
	ranked_url = list(reversed(ranked_url))
	for url_score, url in ranked_url[start_index:end_index]:
		counter+=1
		print url_score

%>
		<tr style="font-size:1.5em">
			<td style="padding-left:0.5em">{{counter}}</td>
			<td style="padding-left:0.5em"><a href="{{url}}">{{url}}</a></td>
		</tr>
    % end
	
	</table>
	<form action="/change_page" method="post">
	<nav align="center">
		<ul>
	% if curr_page > 1:
		<li ><input name="page_num" type="submit" value="prev" /></li>
	% end
	% for page_num in range(1,num_of_page):
	% 	if page_num == curr_page:
		<li ><input style="color:blue;" name="page_num" type="submit" value="{{page_num}}" /></li>
	%   else:
	    <li ><input name="page_num" type="submit" value="{{page_num}}" /></li>
	%   end
	% end
	% if curr_page < num_of_page-1:
		<li ><input name="page_num" type="submit" value="next" /></li>
	% end
		</ul>
	</nav>
	</form>
% 	else:
		<div align="center" style="font-size:1.5em">No results found </div>	
% 	end		

<!--show top 20 most popular keywords if any record exists -->
% if len(record)>0 and user_email:
	<h1 align="center">10 Most recently search words:</h1>
	<table id=”history” style="margin:auto">
		<tr style="font-size:1.5em">
			<th>No.</th>
			<th>Word</th>
			<th>Count</th>
		</tr>
% counter=0
% for key,value in reversed(record.items()):
% counter+=1	
		<tr style="font-size:1em">
			<td align="center">{{counter}}</td>
			<td style="padding-left:1.5em">{{key}}</td>
			<td align="center">{{value}}</td>
		</tr>
% end
	</table>
% end
</body>