# Load packages
#pacman::p_load("tidyverse", "readxl", "ggpubr", "sf",
 #              "RColorBrewer", "randomcoloR", "rnaturalearth")

# Read in the CSV
bvbrc <- read_csv("data/33_BVBRC_laccases.csv") %>%
  dplyr::filter(!is.na(isolation_country)) %>%
  dplyr::filter(!is.na(isolation_source)) %>%
  dplyr::mutate(isolation_sample = case_when(grepl("roadside|soil", isolation_source) ~ "soil", # group
                                             grepl("saltwater|seawater|brine|Lake|water", isolation_source) ~ "surface water",
                                           TRUE ~ isolation_source))
# Fix typos in the geographical locations
bvbrc$isolation_country[bvbrc$isolation_country == "South Korea"] <- c("South Korea")
bvbrc$isolation_country[bvbrc$isolation_country == "USA"]<- c("United States of America")

# Make a map
world <- rnaturalearth::ne_countries(scale = "medium", returnclass = "sf") %>%
  st_transform(., crs = "+proj=moll")
gp2 <- ggplot(world)
countries <- ne_countries(returnclass = "sf")
# Fix strange special characters
countries_center <- st_point_on_surface(countries) %>%
  dplyr::mutate(tokeep = case_when(sovereignt %in% bvbrc$isolation_country ~ sovereignt,
                          sovereignt == "South Korea" ~ "South Korea",
                          sovereignt == "United States of America" ~ "United States of America",
                          TRUE ~ NA)) %>%
  dplyr::filter(!is.na(tokeep))

# Merge
countries_test <- countries_center %>%
  left_join(., bvbrc, by = c("sovereignt" = "isolation_country")) # many-to-one warning message
countries_contam <- countries_center %>%
  left_join(., bvbrc, by = c("sovereignt" = "isolation_country")) %>% # many-to-one warning message
  dplyr::filter(grepl("Italy", sovereignt))

pdf("output/environment_laccase_map.pdf", width = 6, height = 3)
gp2 + 
  geom_sf(data = countries) +
  geom_sf(data = countries_test, size = 3.5, aes(shape = isolation_sample), alpha = 0.5, color = "orange3", line = "black") +
  geom_sf(data = countries_contam, size = 6, shape = 24, alpha = 0.3, fill = "firebrick", line = "black") +
  theme_light() +
  theme(legend.position = "right", legend.title = element_blank())
dev.off()

