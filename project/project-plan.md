# Project Plan

## Summary

<!-- Describe your data science project in max. 5 sentences. -->
This project analyzes the relationship between traffic signs and road accidents in Berlin in 2020.
The study aims to identify which types of traffic signs are most commonly associated with road accidents, and whether certain signs are overrepresented at accident sites.
The findings of this study could be used to inform the development of targeted traffic safety measures aimed at reducing the number of accidents and injuries on Berlin's roads.
The ultimate goal is to provide actionable insights to improve traffic safety in Berlin.


## Rationale

<!-- Outline the impact of the analysis, e.g. which pains it solves. -->
The analysis of the relationship between traffic signs and road accidents in Berlin in 2020 has the potential to improve traffic safety measures in the city.
By identifying which types of signs are most commonly associated with accidents, measures could be taken such as improving the visibility of certain signs, redesigning intersections or roads with a high incidence of accidents, and increasing awareness of particular road hazards. 
Ultimately, this could lead to a reduction in the number of accidents and injuries on the roads, and an overall improvement in traffic safety in Berlin.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource-3502300782194642410: Strassenverkehrsunfälle nach Unfallort in Berlin 2020
* Metadata URL: https://mobilithek.info/offers/-3502300782194642410
* Data URL: https://www.statistik-berlin-brandenburg.de/opendata/AfSBBB_BE_LOR_Strasse_Strassenverkehrsunfaelle_2020_Datensatz.csv
* Data Type: CSV

The above dataset contains road traffic accidents by accident location with street name, GPS coordinates and LOR planning area in Berlin 2020; Accident month, weekday, hour, accident type and category.

### Datasource-7259270924735185334: Traffic Signs: Berlin, 2020
* Metadata URL: https://mobilithek.info/offers/-7259270924735185334
* Data URL: https://www.mcloud.de/downloads/mcloud/722EDEC3-38BA-4FE2-B087-18C0434CA34E/traffic_sign_analysis.json
* Data Type: JSON

The above contains longitude and latitude (WGS84, EPSG:4326) of traffic sign locations and their types in 43 categories, in Berlin in 2020.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->


1. Dataset collection and cleaning [#1][i1]
2. Data exploration and visualization [#2][i2]
3. Statistical analysis [#3][i3]
4. Development of intervention strategies [#4][i4]

[i1]: https://github.com/kreuz1995/2023-amse-template/issues/1
[i2]: https://github.com/kreuz1995/2023-amse-template/issues/2
[i3]: https://github.com/kreuz1995/2023-amse-template/issues/3
[i4]: https://github.com/kreuz1995/2023-amse-template/issues/4
