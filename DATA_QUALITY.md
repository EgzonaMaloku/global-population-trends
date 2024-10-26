# Data Quality

## Summary
A quality assessment of the world population and forecast dataset to ensure reliability and usability for analysis and visualization tasks.

---

### Accuracy

The evaluation of the dataset revealed several accuracy concerns:

- **Missing Countries:** The dataset does not include certain countries, such as Kosovo and Serbia, and fails to adequately represent some islands that are part of other countries.
  
- **Comparison with World Bank Data:** A comparison was performed between our dataset and the World Bank dataset for 10 selected countries over 8 years (from 1960 to 2020, increasing by 10 years). The results of this comparison showed:
  - **Total Population:** Our dataset differs by **2.08%** from the World Bank figures.
  - **Urban Population:** The difference is **2.36%** compared to World Bank data.

While the dataset provides a close approximation of population statistics, the missing countries and percentage differences highlight areas for improvement in accuracy. Further validation from authoritative sources is recommended to enhance the dataset's reliability.


---


### Completeness

The completeness assessment of the dataset identified significant gaps in data availability:

- **Missing Values:** There are **816 missing or empty values** for the following columns:
  - **Migrants (net)**
  - **Median Age**
  - **Fertility Rate**

These missing values indicate a lack of comprehensive data for various countries, which could limit the effectiveness of analyses that rely on these critical demographic indicators.


---

### Timeliness

The timeliness of the dataset is a positive aspect, as it contains world population data that is readily accessible online. This ensures that users can obtain the most current and relevant information when needed. The dataset is designed to reflect ongoing demographic changes, allowing for timely analysis and insights into population trends. Given the dynamic nature of population data, the availability of this information supports informed decision-making and enhances the dataset's overall usability. Regular updates and access to real-time data are essential for maintaining its relevance and effectiveness in research and analysis.


---

### Believability

The dataset's believability is significantly enhanced by its source, Worldometer, which is known for its commitment to providing accurate and timely global statistics. Worldometer operates independently, without political, governmental, or corporate affiliations, ensuring an unbiased representation of data. It is run by an international team of developers, researchers, and volunteers dedicated to making world statistics accessible to a broad audience.

Worldometer has garnered recognition as a trusted authority in the field of statistics, being voted one of the best free reference websites by the American Library Association (ALA). Its data is relied upon by various reputable entities, including the UK Government, Johns Hopkins CSSE, and multiple international organizations. Over the past 15 years, Worldometer’s statistics have been cited in over 10,000 published books and more than 25,000 professional journal articles, further attesting to its credibility.

The dataset obtained from Kaggle was scraped from Worldometer using an open-source Python script, which allows for transparency regarding data collection methods. Given the robust reputation of Worldometer and its extensive use by respected institutions, the dataset can be considered a reliable source for demographic analysis and insights.


---

### Interpretability

The dataset is highly interpretable, characterized by its clear structure and user-friendly presentation. The organization of data allows for straightforward navigation, making it easy for users to understand the various demographic metrics presented. Columns are clearly labeled, and the data types are consistent, facilitating quick comprehension of the information.