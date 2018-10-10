
from sklearn import tree

def get_rf_from_pipeline(pipeline):
    pass

def plot_trees(forest, features, dir_trees):
    
    i_tree = 0
    for tree_in_forest in forest.estimators_:
        path_dot = "{dir}/tree_{i}.{ext}".format(dir=dir_trees, i=i_tree, ext="dot")
        path_png = "{dir}/tree_{i}.{ext}".format(dir=dir_trees, i=i_tree, ext="png")
        cmd_dot = "dot -Tpng {path_dot} -o {path_png}".format(path_dot=path_dot, path_png=path_png)
        with open(path_dot, 'w') as f:
            tree.export_graphviz(tree_in_forest, 
                                     out_file = f, 
                                     feature_names=features,
                                     rounded=True,
                                     filled=True)
        print("wrote", path_dot)
        subprocess.run(cmd_dot, shell=True)
        i_tree = i_tree + 1

#plot_trees(forest, "/storage/temp/trees")


# In[ ]:


import subprocess



# In[ ]:


pipe_rf_500.named_steps['rf']


# In[ ]:


with open("pipe.pickle", "wb") as f:
    pickle.dump(pipe_rf_500, f)


# In[ ]:


with open("pipe.pickle", "rb") as f:
    pipe = pickle.load(f)


# In[ ]:


pipe


# In[ ]:


path_pickle = "/storage/osa/pickles/cm_acled_base_fcast_test_rf_downsampled_sb_6.pickle"
with open(path_pickle, "rb") as f:
    model = pickle.load(f)
    estimator = model['estimator']
    forest = estimator.named_steps['rf']


# In[ ]:


dir_trees = "/storage/osa/trees/"
plot_trees(forest, model['features'], dir_trees)


# In[ ]:


model['features']


# In[147]:


s = "cm_acled_base_fcast_calib_logit_fullsample_sb_36.pickle"
step = re.findall(string=s, pattern="(\d+)")[0]
step

