# Load packages
pacman::p_load("tidyverse", "readxl", "ggpubr", "sf",
               "RColorBrewer", "randomcoloR", "rnaturalearth")

bvbrc <- read_csv("data/BVBRC/33_BVBRC_laccases.csv") %>%
  dplyr::filter(!is.na(isolation_country)) %>%
  dplyr::filter(!is.na(isolation_source)) %>%
  dplyr::mutate(isolation_sample = case_when(grepl("wetland|roadside|soil|seashore", isolation_source) ~ "terrestrial",
                                             grepl("saltwater|seawater|brine|Lake|water", isolation_source) ~ "aquatic",
                                           TRUE ~ isolation_source)) 

# Clean up the country names
bvbrc$isolation_country[bvbrc$isolation_country == "England"] <- "United Kingdom"
bvbrc$isolation_country[bvbrc$isolation_country == "South Korea"] <- c("South Korea")
bvbrc$isolation_country[bvbrc$isolation_country == "USA"]<- c("United States of America")

# Make the global map
world <- rnaturalearth::ne_countries(scale = "medium", returnclass = "sf") %>%
  st_transform(., crs = "+proj=moll")

gp2 <- ggplot(world)
countries <- ne_countries(returnclass = "sf")
countries_center <- st_point_on_surface(countries) %>%
  dplyr::mutate(tokeep = case_when(sovereignt %in% bvbrc$isolation_country ~ sovereignt,
                          sovereignt == "South Korea" ~ "South Korea", # remove special character
                          sovereignt == "South Korea" ~ "South Korea", # remove special character
                          TRUE ~ NA)) %>%
  dplyr::filter(!is.na(tokeep)) %>%
  dplyr::filter(!sovereignt %in% c("United States of America", "Antarctica"))
countries_test <- countries_center %>%
  left_join(., bvbrc, by = c("sovereignt" = "isolation_country"))

countries_contam <- countries_center %>%
  left_join(., bvbrc, by = c("sovereignt" = "isolation_country")) %>%
  dplyr::filter(grepl("chromat|crude", comments))

# Define our two points of interest
points_data <- data.frame(
  name = c("Lake Washington", "Ekho Lake"),
  lon = c(-122.2573, 78.2700),
  lat = c(47.6205, -68.5211)
)

# Convert to spatial object
points_sf <- st_as_sf(points_data, coords = c("lon", "lat"), crs = 4326)

pdf("output/environmental_laccase_map.pdf", width = 6, height = 3)
gp2 + 
  geom_sf(data = countries) +
  geom_sf(data = points_sf, color = "black", shape = 16, size = 2, alpha = 1) +
  geom_sf(data = countries_test, size = 2, aes(shape = isolation_sample), alpha = 1, fill = "black", line = "black") +
  geom_sf(data = countries_contam, size = 2, shape = c(21,21,21,24), fill = "orangered", line = "black") +
  theme_light() +
#  scale_fill_manual(values = rep("orange1", 25)) +
  theme(legend.position = "right", legend.title = element_blank())
dev.off()




