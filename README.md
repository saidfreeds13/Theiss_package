# Former industrial neighborhoods of Saint Petersburg: assessing relationships between street-network morphology and social organization of space. 
*Developed by Bereiya Said, 2nd year master student of IDU ITMO*  
*Supervised by*

## Contents ##
A. [The Block-Scheme of the method](https://github.com/saidfreeds13/Theiss_package/tree/master?tab=readme-ov-file#a-the-block-scheme-of-the-method)   
B. [The method's explanation](https://github.com/saidfreeds13/Theiss_package/tree/master?tab=readme-ov-file#b-the-methods-explanation)  
C. [Installation](https://github.com/saidfreeds13/Theiss_package/tree/master?tab=readme-ov-file#c-method-installation)  
D. [Application illustration](https://github.com/saidfreeds13/Theiss_package/tree/master?tab=readme-ov-file#c-method-installation)  
E. [Publications](https://github.com/saidfreeds13/Theiss_package/tree/master?tab=readme-ov-file#publications)

## Introduction 
Nowadays, more often than not former industrial areas experience the consequences of being "left-behind"[^1]. "Left-behindness" entails a variety of socio-spatial externalities such as physical deterioration of infrastructure[^2], an increased social tension[^3], stigmatization[^4]. These are what an American geographer Ed Soja called "metropolarities"[^5]: new (nonlinear) forms of social inequality and increased social contrasts. To initiate a more evidence-based regeneration projects and policy for these areas, a deep understanding of the exisitng space-society relationships is required, more so in the context of post-socialist cities [^6]. It is in the scope of this thesis to identify and characterise the forms of (paradoxical) relationships between the spatial morphology and social organization of space in the former industrial neighborhoods. A street-network, and a street as its element, are suggested as a perspective unit of analysis, allowing for porous movement between a micro-level and a meso-level scales. The city of interest is St. Petersburg (Russia) which has an immense territory of previous industrial use now referred to as "Gray Belt". The theoretical foundation of the research is the movement dubbed "Spatial Cultures" which emerged under the influence of Émile Durkheim’s sociology and the Space Syntax theory of Hillier and Hanson[^7].

[^1]: Soja E. W. My Los Angeles: From Urban Restructuring to Regional Urbanization. Berkeley, Los Angeles, London: University of California Press, 2014.
[^2]: Fraser A., Clark A. Damaged hardmen: Organized crime and the half-life of deindustrialization // Br. J. Sociol. — 2021. — Vol. 72. — P. 1062–1076. — DOI: https://doi.org/10.1111/1468-4446.12828.
[^3]: Linkon S. L. The half-life of deindustrialization: Working-class writing about economic restructuring. — Ann Arbor: University of Michigan Press, 2018. 
[^4]: Vanke A. Co-existing structures of feeling: Senses and imaginaries of industrial neighbourhoods // The Sociological Review. — 2024. — Vol. 72, № 2. — P. 276–300. — DOI: 10.1177/00380261221149540.
[^5]: Soja E. W. Postmetropolis. Critical Studies of Cities and Regions. Malden: Blackwell, 2000. Pp. 264–297
[^6]: Golubchikov O., Badyina A., Makhrova A. The Hybrid Spatialities of Transition: Capitalism, Legacy and Uneven Urban Economic Restructuring // Urban Studies. 2014. Vol. 51, № 4. P. 617–633.
[^7]: Spatial Cultures: Towards a New Social Morphology of Cities Past and Present / Ed. by S. Griffiths, A. Von Lünen. — London; New York: Routledge, 2016. — P. 23.

## A. The Block-Scheme of the method ##
Street-network morphology is operationalized via Space Syntax. Its key measuresare Integration and Choice calculated for street segments. One can prepare the dataset with syntactic measures in a QGis module "Graph Analysis". 
Social organization of space is uderstood as a distribution of urban functions across a neighborhood. The operationalization for the social organization is done via a functional diveristy metric, showing how diverse and dense the social appropriation of each street's segment is.  

<p align="center">
  <img width="1080" height="1080" alt="BS_methodology drawio" src="https://github.com/saidfreeds13/Theiss_package/blob/0bbd5afda8f602ead7da3659a5dacf80bcbe6af1/canvas.png">
</p>
<p align= "center"> *The block-scheme of the method, author: Bereiya Said 2nd year master student of IDU ITMO* </p>

## B. The method's explanation ## 
The main ETL-algorithms are packed in the library "streets_syntax_social" (installation instructions [below](https://github.com/saidfreeds13/Theiss_package/blob/master/README.md#c-method-installation)

### Algorithm 1. A street-network dataset with syntactic and functional diversity metrics  ###
The key function of the method is "streets_social_sdataset()".
``` 
streets_social_sdataset(
    uf = ,
    streets_m = ,
    package = "",
    save_file="",
    functions_subgroup_col_name = "",
    functions_subgroup_col_alias = "",
    urban_function_id = "",
    urban_function_type_name = "",
    morpho_metrics_list_cols = ["","", "", ""]
    )
```
Taking a street-network with morphological values and the urban functions (points), it builds a geo-dataset of street segmetns (LineString) with columns containing the syntactic and functional diversity metrics. Depending on the parameters set by a user, the number of characteristical columns may vary from four up to thirty. 

#### Algorithm 1. Visualization ####
The results are then visualized with a function "visuals", essentially generating the choropleths of all metrics (both syntactic and functional). 
These maps can be compared between each other, especially those of morphology and functional diversity.    

#### Algorithm 1. Interpretation ####
As a result, a user arrives at two distinct street hierarchies: the one of physcial dimension and the one of social dimension of a network. The distribution of syntactic values of all streets reveals the patterns of to-/through- movement logic, while the distribution of functional diversity metrics identifies socially appropriated of to-/through- movement logic. Obviously, these two hierarchies are bound to have mismatches; however, the nature and the intensity of the mismatches are dependent on the territorial assets and issues.  

### Algorithm 2. Mismatches' identification ###
However, at this stage the relatiosnhips between these two hiararchies lack the direct systematic juxtoposition. The function "streets_mismatched" addresses the issue with the following formula:  


<p align="center"> 
  $$\Large(a \cdot Int_i + b \cdot Ch_i) - FD_i = mismatch_i$$ 

  <details> <summary> Open the variables' description  </summary>

  *a*: weight of integration measure;  
  *b*: weight of choice measure;  
  *Int_i*: integration value for an i-segment;  
  *Ch_i*: choice value for an i-segment;  
  *FD_i*: functional diversity metric for an i-segment;  
  *mismatch_i*: mismatch between social and morphological values of an i-segment. 

</details>
</p> 
  
  
#### The python-algorithm *streets_mismatched()* has the following parameters:
> [!IMPORTANT]
> All metrics must be normalized for mismatches to be adequately calculated .   
> The best way would be to run apply the first algorithm "streets_social_sdataset()" with packages containg normalized metrics (Basic_plus, Advanced_plus or All) 
```
streets_mismatched(
    data, # the dataset with normalized syntactic measures and functional urban metrics
    functional_metric, # the column that stores the functional metric 
    int_g, # Integration metric column (global)
    int_l, # Integration metric column (local)
    ch_g, # Choice metric column (global)
    ch_l # Choice metric column (local)
    )
```


After the activation of *streets_mismatched()*, the function would ask for the weights of syntactic measures a and b at:  
1. Average scale
2. Global scale  
3. Local scale   

### Algorithm 2. Interpretation
Two street hiearhies are exmpolicitly compared  

## C. Method installation ##
In order to install the package, containng the method use python environmnent such as Colab, Jupeter Notebooks. 

Firstly, clone the repo:
``` 
!git clone https://github.com/saidfreeds13/Theiss_package/
```
Then, install the git package and extract the package:
```
!pip install git+https://github.com/saidfreeds13/Theiss_package.git

!pip install theiss-package
```
Finally, import the method:
```
import streets_syntax_social 
```
## D. Experimental application ##
This section contains snippets from the experimental application of a method, for more detailed examples see the folder "Experiments"  

### The results from the algorithm 1 (a possible representation) 
<p align="center">
  <img width="1080" height="1080" alt="BS_methodology drawio" src="https://github.com/saidfreeds13/Theiss_package/blob/60ae54740a34e6ecc8eee71a1e92f71bb4857e7c/Dashboard%20example.png">
</p>
<p align= "center"> Dashboard for the comparison of street-network morphology and social organization of space in southwestern part of the Grey Belt (St. Petersburg), author: Bereiya Said 2nd year master student of IDU ITMO </p>

### The results from the algorithm 2 (a possible representation) 

#### Mismatches of the whole street-network

#### Mismatches on a single street-level


## Publications ##
1. Bereiya S.A. The Street-Road Network of a Post-Socialist City as an Inherited System: Identifying Relationships between Morphology and Social Organization Using Tools of Digital Urban Studies // Information Technologies in Humanitarian Research: Proceedings of the International Scientific-Practical Conference, Krasnoyarsk, November 10–13, 2025 / – Krasnoyarsk: Siberian Federal University, 2026. - Pp. 98-103. - [URL.](https://bik.sfu-kras.ru/ft/LIB2/ELIB/u004/free/i-205105528.pdf#%5B%7B%22num%22%3A314%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22FitH%22%7D%2C744%5D) (*In Russian*)

## Experimental application ##

---
