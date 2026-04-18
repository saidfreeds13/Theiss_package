# Former industrial neighborhoods of Saint Petersburg: assessing relationships between street-network morphology and social organization of space 
*Developed by Bereiya Said Adnanovich, a master student of IDU, ITMO University*  
*Supervised by Baltyzhakova Tatiana Igorevna, an associate professor of IDU, ITMO University*

## Contents ##
A. [The Block-Scheme of the method](https://github.com/saidfreeds13/Theiss_package/tree/master?tab=readme-ov-file#a-the-block-scheme-of-the-method)   
B. [The method's explanation](https://github.com/saidfreeds13/Theiss_package/tree/master?tab=readme-ov-file#b-the-methods-explanation)  
C. [Installation](https://github.com/saidfreeds13/Theiss_package/tree/master?tab=readme-ov-file#c-method-installation)  
D. [Application illustration](https://github.com/saidfreeds13/Theiss_package/tree/master?tab=readme-ov-file#c-method-installation)  
E. [Publications](https://github.com/saidfreeds13/Theiss_package/tree/master?tab=readme-ov-file#e-publications)

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
  <img width="1080" height="1080" alt="BS_methodology drawio" src="https://github.com/saidfreeds13/Social_syntax_of_street_networks/blob/14e643149582337d9ea85f7f86f2c13e0711ac99/The%20pipeline.png">
</p> 
<p align= "center"> *The pipeline of the geo-method, author: Bereiya Said 2nd year master student of IDU ITMO* </p>

## B. The method's explanation ## 
The developed ETL-algorithms are packed in the SocSynStreets package (installation instructions are [below](https://github.com/saidfreeds13/Theiss_package/blob/master/README.md#c-method-installation))

### Algorithm 1. A street-network dataset with syntactic and functional diversity metrics  ###
The key function of the method is "streets_social_sdataset()".
``` 
streets_social_sdataset(
    uf=,                           #Urban functions dataset in points (crs:WKT3857)
    streets_m,                      #Street-network morphology dataset in MultiLines (crs:WKT3857)
    urban_function_id,                   #unique identifier of an urban function
    urban_function_type_name,                 #the category column denoting the type of the urban function 
    morpho_metrics_list_cols,                 #the list of columns that contain the syntactic measures
    functions_subgroup_col_name = None,         #subgrouping some kinds of functions denoted by a separate column
    functions_subgroup_col_alias=None,           #the alias for the new subgouped diversity indexes 
    save_file = ("csv","geojson", "none"),             #the format of the saving the resulting file
    package = [
      "Basic",
      "Basic_plus",
      "Advanced",
      "Advanced_plus",
      "All" ]                                        #choice of metrics (depends on a stakeholder's needs)
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
> All metrics must be normalized for mismatches to be adequately calculated.   
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
>[!NOTE]
>The street segments that have no urban functions in the immediate street space are ommited in the final visualization and are dimmed NaN in the dataset.

After the activation of *streets_mismatched()*, the function would ask for the weights of syntactic measures a (Integration) and b (Choice) at:  
1. Average scale (average between local and global syntactic measures)
2. Global scale  (only global syntactic measures are included in the relationship identification)
3. Local scale   (only local syntactic measures are included in the relationship identification)

```
mism plot
```

### Algorithm 2. Interpretation (In dev)
As a result of the second algorithm, two street hierarchies are mathematically compared and the relationships between the two could be identified as matching or mismatching. 
Importantly, the definition of (mis-)matching is fluid and dependent on an analyst's specification. Here, we provide a few examples of such definition and its impact on a pipeline realization.   
1. Is social infrastructure generally located in the most integrated streets?
2. Are the most functionally diverse areas located on the well-integrated and well-porous streets of a neighborhood?
3. Are the less socially-engaged streets more likely to be found on the least integrated streets?   

## C. Method installation ##
In order to install the package, containng the method use python environmnent such as Colab, Jupeter Notebooks. 

Firstly, clone the repo:
``` 
!git clone https://github.com/saidfreeds13/Social_syntax_of_street_networks/
```
Then, install the git package and the needed libraries:
```
!pip install git+https://github.com/saidfreeds13/Social_syntax_of_street_networks.git
!pip install -r /content/Social_syntax_of_street_networks/Libraries.TXT
```
Finally, import the method:
```
import Social_syntax_of_street_networks.SocSynStreets
```
## D. Experimental application (In dev)
This section contains snippets from the experimental application of a method, for more detailed examples see the folder "Experiments"  

### The results from the algorithm 1 (a possible representation) 
<p align="center">
  <img width="1080" height="1080" alt="BS_methodology drawio" src="https://github.com/saidfreeds13/Theiss_package/blob/60ae54740a34e6ecc8eee71a1e92f71bb4857e7c/Dashboard%20example.png">
</p>
<p align= "center"> Dashboard for the comparison of street-network morphology and social organization of space in southwestern part of the Grey Belt (St. Petersburg), author: Bereiya Said 2nd year master student of IDU ITMO </p>

### The results from the algorithm 2 (a possible representation) (In dev)

#### Mismatches of the whole street-network
<p align="center">
  <img width="900" height="900" alt="BS_methodology drawio" src="https://github.com/saidfreeds13/Theiss_package/blob/7a8440c81dc3152641365c516d53686dfe4639f0/mismatches/s0_mismathes_Natural_Breaks_basemap.png">
</p>
<p align= "center">

#### Mismatches on a single street-level (In dev)


## E. Publications ##
1. Bereiya S.A. The Street-Road Network of a Post-Socialist City as an Inherited System: Identifying Relationships between Morphology and Social Organization Using Tools of Digital Urban Studies // Information Technologies in Humanitarian Research: Proceedings of the International Scientific-Practical Conference, Krasnoyarsk, November 10–13, 2025 / – Krasnoyarsk: Siberian Federal University, 2026. - Pp. 98-103. - [URL.](https://bik.sfu-kras.ru/ft/LIB2/ELIB/u004/free/i-205105528.pdf#%5B%7B%22num%22%3A314%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22FitH%22%7D%2C744%5D) (*In Russian*)

---
