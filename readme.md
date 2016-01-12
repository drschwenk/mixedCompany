<br><br>

##Overview
<br><br>

We’re in the midst of a cocktail renaissance. Hoping to contribute to this recent resurgence, I’ve created MixedCompany—a tool for recommending novel ingredient pairings and substitutions in cocktails. The ingredient-flavor network latent in the world of mixed drinks contains a great deal of information about our preferences for flavor combinations. I build and exploit this network to suggest ingredients that should pair well together, but have not appeared together before in existing cocktail recipes. Interesting new twists on famous cocktail recipes, backed up by flavor data, are waiting to be explored with MixedCompany.
I plan to follow the example of 

[Ahn, Ahnert, Bagrow and Barabási](http://www.nature.com/articles/srep00196 "Title")
by exploring the [ingredient-flavor network](https://en.wikipedia.org/wiki/Ingredient-flavor_network 'Title') within the world of cocktails. I will build this network by gathering and blending data from several sources, and then apply network analysis techniques to investigate the flavor parings the occur in mixology.

<br><br>
![many overlap](img/overlapping_ingredients.png =319x200)
![many overlap](img/overlapping_ingredients_few.png =319x200)
<br><br>
<br><br>


##Dataset
<br><br>





<br><br>
##Data Sources
<br><br>



[Burdock, G. A. Fenaroli's handbook of flavor ingredients (CRC Press, 2004), 5th edn.](https://books.google.com/books?id=A8OyTzGGJhYC&printsec=frontcover&source=gbs_ge_summary_r&cad=0#v=onepage&q&f=false "Title")

[wikipedia](https://en.wikipedia.org/wiki/List_of_cocktails "Title")

[liquor.com ~ 1200](http://liquor.com/recipes/ "Title")

[webtender ~ 500](http://wiki.webtender.com/wiki/Category%3aRecipes "Title")

[NYT drinks](http://topics.nytimes.com/top/features/magazine/columns/drink/index.html "Title")
<br><br>

##Methods
<br><br>

Sanitizing the flavor and recipe data will be a major challenge for this project.

I have the flavor data in plaintext, but it is not in a tabular, searchable form. I will need to parse the document, recovering the words that I'm interested in. The OCR I've done is good, but not perfect. I will need to correct any misidentified characters in order to make the matches between flavor compounds that are the foundation of the network. NLP techniques should help here. 

Cocktail recipes are available numerous places on the internet, and I'm confident I can scrape many of them. As above, parsing the pages and eliminating duplicate recipes may be challenging (I imagine everyone will have a recipe for a gin and tonic). 

A third data component will be needed to link the ingredients in some less common liqueurs, Apéritifs etc. to the flavor compounds in Fenaroli's handbook. I've underestimated this issue, and it's unlikely that I'll get a complete ingredient list for many products. I will need to look at the frequency of these ingredients in the recipe dataset before knowing how big of a problem this represents.

Building the flavor ingredient network seems reasonable, and it could be done with either networkx or graphlab. 

I like the figures in the paper, and will attempt reproduce their look with either Bokeh or D3 (if necessary). 
<br><br>

##Results
<br><br>
![many overlap](img/light_pair_corr.png =670x344)
w





