"""
CKAN api

- list_datasets(): return dataset IDs list
- list_datasets_with_tag(tag): return dataset IDs list for given tag
- list_groups()
- list_tags()

- info_dataset(id): return json object with dataset info
- info_dataset_resume(id): return reduced json object with dataset info
- info_group(id)
- info_tag(id)

- search_dataset(query)
- search_resource(query)

- recent_activity()

- top_tags(n)

- get_resource(url)

- get_data_from_repository(): return csv data from ckan website as list of dicts - [{'name': ..., 'csv': ...}, ...]

"""

import requests, json, time
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.web import JsonLexer
from log import *

class CKAN:

	def __init__(self, base_url = "http://dados.gov.br"):
		self.base_url = base_url

	def get(self, endpoint):
		response = requests.get(self.base_url + endpoint)
		try: return {"status": response.status_code, "data": json.loads(response.text) }
		except json.decoder.JSONDecodeError: return {"status": response.status_code, "data": {} }

	def list_datasets(self):
		request = self.get("/api/3/action/package_list")
		datasets = request["data"]["result"]
		return datasets

	def list_datasets_with_tag(self, tag):
		request = self.get(f"/api/3/action/package_search?fq=tags:{tag}")
		return request["data"]["result"]["results"]

	def list_groups(self):
		return self.get("/api/3/action/group_list")

	def list_tags(self):
		request = self.get("/api/3/action/tag_list")
		return request["data"]["result"]

	def info_dataset(self, id):
		return self.get(f"/api/3/action/package_show?id={id}")

	def info_dataset_resume_by_id(self, id):
		info, dict = self.info_dataset(id), {}
		if(info["status"] != 200): return {}
		dict["name"] = info["data"]["result"]["name"]
		dict["author"] = info["data"]["result"]["author"]
		dict["modified"] = info["data"]["result"]["metadata_modified"]
		dict["private"] = info["data"]["result"]["private"]
		dict["state"] = info["data"]["result"]["state"]
		dict["url"] = info["data"]["result"]["url"]
		dict["resources"] = [(resource["format"], resource["url"]) for resource in info["data"]["result"]["resources"]]
		dict["tags"] = [tag["name"] for tag in info["data"]["result"]["tags"]]
		return dict

	def info_dataset_resume_by_json(self, json):
		dict = {}
		dict["name"] = json["name"]
		dict["author"] = json["author"]
		dict["modified"] = json["metadata_modified"]
		dict["private"] = json["private"]
		dict["state"] = json["state"]
		dict["url"] = json["url"]
		dict["resources"] = [(resource["format"], resource["url"]) for resource in json["resources"]]
		dict["tags"] = [tag["name"] for tag in json["tags"]]
		return dict

	def info_dataset_resume(self, object):
		if isinstance(object, dict): return self.info_dataset_resume_by_json(object)
		else: return self.info_dataset_resume_by_id(object)

	def info_tag(self, id):
		return self.get(f"/api/3/action/tag_show?id={id}")

	def info_group(self, id):
		return self.get(f"/api/3/action/group_show?id={id}")

	def search_dataset(self, query):
		request = self.get(f"/api/3/action/package_search?q={query}")
		return request["data"]["result"]["results"]

	def search_resource(self, query):
		return self.get(f"/api/3/action/resource_search?query={query}")

	def recent_activity(self):
		return self.get("/api/3/action/recently_changed_packages_activity_list")

	def top_tags(self, n = 10):
		return self.get(f"/api/action/package_search?facet.field=[%22tags%22]&facet.limit={n}&rows=0")

	def get_resource(self, url):
		r = requests.get(url, stream = True, timeout = 5, allow_redirects=True)
		r.raw.decode_content = True
		return r


class Utils:
	
	@staticmethod
	def pprint(jsonText):
		formatted = json.dumps(jsonText, indent=4, sort_keys=True)
		colorful = highlight(formatted, lexer=JsonLexer(), formatter=TerminalFormatter())
		print(colorful)

	@staticmethod
	def is_json(object):
  		try: json.loads(object)
  		except ValueError: return False
  		return True

def get_data_from_repository():
	ckan = CKAN()
	datasets = ckan.list_datasets()

	csv_list = []
	datasets_used = []
	base_index = 1000
	limit_index = base_index + 50
	for i in range(base_index, limit_index):
		info = ckan.info_dataset_resume(datasets[i])
		for rsrc in info["resources"]:
			if rsrc[0] == "CSV":
				csv = ckan.get_resource(rsrc[1])
				if csv.status_code == 200:
					if info["name"] not in datasets_used:
						entry = {'name': info["name"], 'csv': csv.text}
						#print(entry)
						csv_list.append(entry)
						datasets_used.append(info["name"])
		#Utils.pprint(info)
	return csv_list

if __name__ == '__main__':

	Log.Configure()
	Log.Info("Application started")

	#Utils.pprint(ckan.top_tags())
	#datasets = ckan.search_dataset("educação")
	#datasets = ckan.list_datasets_with_tag("orçamento")
	
	start_time = time.time()
	all_data = get_data_from_repository()
	print('size of csv list: ', len(all_data))
	print("--- %s seconds ---" % (time.time() - start_time))
	