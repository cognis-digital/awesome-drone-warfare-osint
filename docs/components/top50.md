# Top-50 most-found components

Computed live from `data/components.csv`. The current Top-15 manufacturers
(by number of identified components) match the [KSE Institute 2023
analysis](https://kse.ua/about-the-school/news/foreign-components-in-russian-military-drones/)
finding that ~69 % of components come from US-owned firms.

![Top manufacturers](../../images/top_manufacturers.png)

![Country of origin](../../images/origin_countries_top10.png)

Regenerate with:

```bash
jupyter nbconvert --to html --execute notebooks/01_component_origin_map.ipynb
```
