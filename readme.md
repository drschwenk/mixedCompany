  Dustin Schwenk, 12/14
<br><br>

##Summary
<br><br>
I plan to follow the example of 
[Ahn, Ahnert, Bagrow and Barabási](http://www.nature.com/articles/srep00196 "Title")
by exploring the [ingredient-flavor network](https://en.wikipedia.org/wiki/Ingredient-flavor_network 'Title') within the world of cocktails. I will build this network by gathering and blending data from several sources, and then apply network analysis techniques to investigate the flavor parings the occur in mixology.
<br><br>

##Motivation
<br><br>
I enjoyed reading Ahn, Ahnert, Bagrow and Barabási paper when it was published, and generally find the ideas underlying the flavor-ingredient network interesting. I enjoy mixed drinks and novel flavor pairings, and it seems like the same techniques should apply to world of cocktails.
<br><br>
##Deliverables: How will you demonstrate your project? 
<br><br>
I will generate a set of figures that illustrate my findings in a pithy, visual way. I've included examples of the sort of figures I have in mind from the paper I've cited. Imagine these with common cocktail ingredients in place of the foods shown.  

If I begin to find anything interesting (like the differences found for Western and East Asian Cuisine), I will spend more time on the analysis. I envision this fueling my presentation as well as a blog post (with the potential for interactive visualizations). 

If time permits, I would like to build a simple web app that would allow a user to generate novel flavor pairing based on the flavor-ingredient network that I build. This could be one or more of-

1. A randomized recipe with an accompanying score signifying 'goodness' in some way. I'm being intentionally vague here, but I imagine that there should be some score based on the weights of the edges for the new 'comp-tail' (computationally generated cocktail...) in the the flavor-ingredient graph.
2. As the user enters ingredients, the app will begin to make suggestions for additions with complementary flavors. 
3. The user starts with a classic cocktail of some sort. The app suggests a replacement for one of the ingredients that will still work according to the network. 

__Example figures__
<br><br>
![example fig 1](img/flavor_network_fig1.jpg =488x400)
<br><br>

![example fig 2](img/flavor_network_fig2.jpg =488x307)
<br><br>

![example fig 3](img/flavor_network_fig3.jpg =488x310)

<br><br>
##Data Sources
<br><br>

I will use Fenaroli's handbook as a reference for the flavor compounds. I've already done OCR on the book, and I have reasonably good plaintext that I can work with. As for the recipes, there are numerous books and websites to choose from. The ones I've checked seem to be easily scrapable, and I think the choice of sources will be informed by some meta feature of the recipe (date of creation, popularity, region of origin, etc.) that I might decide to investigate. If this proves to be an issue, there are some pre-assembled databases in existence that I can turn to. 

[Burdock, G. A. Fenaroli's handbook of flavor ingredients (CRC Press, 2004), 5th edn.](https://books.google.com/books?id=A8OyTzGGJhYC&printsec=frontcover&source=gbs_ge_summary_r&cad=0#v=onepage&q&f=false "Title")

[wikipedia](https://en.wikipedia.org/wiki/List_of_cocktails "Title")

[liquor.com ~ 1200](http://liquor.com/recipes/ "Title")

[webtender ~ 500](http://wiki.webtender.com/wiki/Category%3aRecipes "Title")

[NYT drinks](http://topics.nytimes.com/top/features/magazine/columns/drink/index.html "Title")
<br><br>

##Process
<br><br>

Sanitizing the flavor and recipe data will be a major challenge for this project.

I have the flavor data in plaintext, but it is not in a tabular, searchable form. I will need to parse the document, recovering the words that I'm interested in. The OCR I've done is good, but not perfect. I will need to correct any misidentified characters in order to make the matches between flavor compounds that are the foundation of the network. NLP techniques should help here. 

Cocktail recipes are available numerous places on the internet, and I'm confident I can scrape many of them. As above, parsing the pages and eliminating duplicate recipes may be challenging (I imagine everyone will have a recipe for a gin and tonic). 

A third data component will be needed to link the ingredients in some less common liqueurs, Apéritifs etc. to the flavor compounds in Fenaroli's handbook. I've underestimated this issue, and it's unlikely that I'll get a complete ingredient list for many products. I will need to look at the frequency of these ingredients in the recipe dataset before knowing how big of a problem this represents.

Building the flavor ingredient network seems reasonable, and it could be done with either networkx or graphlab. 

I like the figures in the paper, and will attempt reproduce their look with either Bokeh or D3 (if necessary). 





