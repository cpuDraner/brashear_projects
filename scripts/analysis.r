library(gridExtra)
library(janitor)
library(readxl)
library(dplyr)
library(survival)
library(caret)
library(car)
library(ggplot2)
library(dplyr)
summary(best_model)

#r code initially by Lona Adams
pittsburgh_census <- data.frame(
  variable = c(
    "Population_2024",
    "Population_2020",
    "Under_5_percent",
    "Under_18_percent",
    "Over_65_percent",
    "Female_percent",
    "White_percent",
    "Black_percent",
    "Asian_percent",
    "Hispanic_percent",
    "Foreign_born_percent",
    "Owner_occupied_percent",
    "Median_home_value",
    "Median_rent",
    "Households",
    "Persons_per_household",
    "Broadband_percent",
    "Highschool_percent",
    "Bachelors_percent",
    "Disability_under65_percent",
    "Uninsured_under65_percent",
    "Labor_force_percent",
    "Median_household_income",
    "Per_capita_income",
    "Poverty_percent",
    "Mean_travel_time",
    "Land_area_sq_miles",
    "Population_density"
  ),
  value = c(
    307668,
    302971,
    4.6,
    14.6,
    15.6,
    51.3,
    62.7,
    22.3,
    6.2,
    4.5,
    9.5,
    47.7,
    205800,
    1261,
    138188,
    2.03,
    90.4,
    94.4,
    49.1,
    10.4,
    5.6,
    64.3,
    65742,
    45385,
    20.1,
    22.7,
    55.38,
    5471.3
  )
)
pantry_data <- read_excel("data\\pantry_data.xlsx")
file_path <- "data\\pantry_data.xlsx"
sheets <- excel_sheets(file_path)

pantry_data <- sheets %>%
  lapply(function(x)
    read_excel(file_path,
               sheet = x,
               col_types = "text")   # <- FORCE everything to text
  ) %>%
  bind_rows()

pantry_data <- pantry_data %>%
  clean_names()

sheets <- sheets[!grepl("Export Summary", sheets, ignore.case = TRUE)]

pantry_data <- sheets %>%
  lapply(function(x)
    read_excel(file_path,
               sheet = x,
               col_types = "text")
  ) %>%
  bind_rows()



pantry_data <- pantry_data %>%
  clean_names()

pantry_data <- pantry_data %>%
  rename(
    age_group = what_age_group_does_the_client_belong_to_head_of_household,
    monthly_income = what_is_the_total_monthly_household_income_combined_gross_monthly_for_all_income_types_and_members_with_income,
    received_last_month = did_you_receive_food_last_month,
    pickup_date = which_date_will_you_pick_up,
    new_client = new_client_confirm_if_new_registration_completed_in_2025
  )

pantry_data <- pantry_data %>%
  mutate(
    race_clean = case_when(
      race %in% c("African American", "Black or African American") ~ "Black/African American",
      race %in% c("Caucasian", "Caucasian or White") ~ "White",
      race %in% c("American Indian or Alaska Native", "Native Indian") ~ "American Indian/Alaska Native",
      TRUE ~ race
    )
  )

pantry_data <- pantry_data %>%
  mutate(
    income_cat = case_when(
      is.na(monthly_income) ~ "Missing",
      monthly_income < 1000 ~ "<1000",
      monthly_income < 2000 ~ "1000-1999",
      monthly_income < 3000 ~ "2000-2999",
      TRUE ~ "3000+"
    )
  )

pantry_race_dist <- pantry_data %>%
  count(race_clean) %>%
  mutate(percent = n / sum(n) * 100)

"""93% (1236 out of 1329) of entries are NA. Among the non-missing responses:

Black/African American: 42 (3.2% of total)

White: 35 (2.6% of total)

Other, Bi-Racial, etc.: 16 (1.2% of total)
"""

pantry_data <- pantry_data %>%
  mutate(
    received_last_month = trimws(tolower(received_last_month)),
    returned = ifelse(received_last_month == "yes", 1, 0)
  )

#table(pantry_data$returned)

"568 clients are new (answered no to receiving food last month)

761 clients are returning (answered yes to receiving food last month)

older model
"

pantry_data <- pantry_data %>%
  mutate(
    received_last_month = trimws(tolower(received_last_month)),
    returned = ifelse(received_last_month == "yes", 1, 0)
  )

model_return <- glm(returned ~ income_cat + family_size + age_group,
                    family = binomial,
                    data = pantry_data)

summary(model_return)

table(pantry_data$received_last_month, useNA="ifany")

colSums(is.na(pantry_data[, c("monthly_income", "family_size", "age_group")]))

pantry_data$family_size <- as.numeric(gsub("[^0-9]", "", pantry_data$family_size))

"new model :P"

model_return <- glm(returned ~ income_cat + family_size + age_group,
                    family = binomial,
                    data = pantry_data)

#summary(model_return)

"
Income: Clients with missing income data were much more likely to be returning clients (p-value = 4.66e-06)

Family Size: This variable was not a significant predictor of return status (p-value = 0.697)

Age Group: None of the age group categories showed statistical significance. The only one approaching significance was the 60-69 age group (p-value = 0.0897)
"

pantry_data$timestamp <- as.Date(
  as.numeric(pantry_data$timestamp),
  origin = "1899-12-30"
)

survival_data <- pantry_data %>%
  group_by(client_id) %>%
  summarise(
    first_visit = min(timestamp, na.rm = TRUE),
    last_visit  = max(timestamp, na.rm = TRUE),
    duration_days = as.numeric(last_visit - first_visit),
    total_visits = n()
  )

survival_data$event <- ifelse(survival_data$total_visits > 1, 1, 0)

km_income <- survfit(
  Surv(duration_days, event) ~ income_cat,
  data = survival_data
)

"income"

survival_data <- survival_data %>%
  left_join(
    pantry_data %>% select(client_id, income_cat) %>% distinct(),
    by = "client_id"
  )

plot(km_income,
     col = 1:5,
     xlab = "Days in Program",
     ylab = "Probability of Remaining Active")

legend("topright",
       legend = levels(as.factor(survival_data$income_cat)),
       col = 1:5,
       lty = 1)

library(survival)

study_end <- max(pantry_data$timestamp, na.rm = TRUE)

survival_data <- pantry_data %>%
  group_by(client_id) %>%
  summarise(
    first_visit = min(timestamp),
    last_visit  = max(timestamp),
    duration_days = as.numeric(last_visit - first_visit),
    total_visits = n()
  )

survival_data$event <- ifelse(
  survival_data$last_visit < study_end,
  1,   # they stopped before study ended
  0    # censored (still active)
)

"not income"

surv_object <- Surv(
  time = survival_data$duration_days,
  event = survival_data$event
)

km_fit <- survfit(surv_object ~ 1)

plot(km_fit,
     xlab = "Days in Program",
     ylab = "Probability of Remaining Active",
     main = "Kaplan-Meier Survival Curve")

"What's being measured

Time: Days between a client's first visit and last visit

Event: When a client stops coming (drops out)

Censoring: When we lose track of a client because there's no more data

Event = 1: Client's last visit was BEFORE the data ends → they dropped out (experienced the event)

Event = 0: Client's last visit was AT the data ending → they were still active (censored)

Overall
"

# Final model using ALL data
pantry_clean <- pantry_data %>%
  mutate(
    # Core variables - no missing data
    household_size = as.numeric(gsub("[^0-9].*$", "", family_size)),
    age_group = case_when(
      grepl("18|25|34", age_group) ~ "Young Adult",
      grepl("35|44|45|54|59", age_group) ~ "Middle Adult",
      grepl("60|64|65|69|70|74|75", age_group) ~ "Senior",
      TRUE ~ "Other"
    ),

    # Income - keep missing as category
    income_status = case_when(
      is.na(monthly_income) ~ "Not Reported",
      suppressWarnings(as.numeric(monthly_income) < 1000) ~ "Low",
      suppressWarnings(as.numeric(monthly_income) < 3000) ~ "Medium",
      suppressWarnings(as.numeric(monthly_income) >= 3000) ~ "High",
      TRUE ~ "Not Reported"
    ),

    # Pets - assume no if missing
    has_pets = case_when(
      is.na(pets) ~ 0,
      tolower(pets) == "yes" ~ 1,
      TRUE ~ 0
    ),

    # Returned
    is_returning = returned
  )

# Model on ALL 1329 rows
best_model <- glm(
  is_returning ~ household_size + age_group + income_status + has_pets,
  family = binomial,
  data = pantry_clean
)

# Check what drives the "Missing" effect
pantry_clean %>%
  group_by(income_status) %>%
  summarise(
    count = n(),
    return_rate = mean(is_returning),
    avg_family_size = mean(household_size)
  )

library(ggplot2)

# Create the summary data
income_summary <- pantry_clean %>%
  group_by(income_status) %>%
  summarise(
    count = n(),
    return_rate = mean(is_returning),
    se = sqrt((return_rate * (1 - return_rate)) / count)  # Standard error
  ) %>%
  # Reorder factor levels for better display
  mutate(income_status = factor(income_status,
                                levels = c("Low", "Medium", "High", "Not Reported")))

# Bar chart with error bars
ggplot(income_summary, aes(x = income_status, y = return_rate, fill = income_status)) +
  geom_col() +
  geom_errorbar(aes(ymin = return_rate - se, ymax = return_rate + se), width = 0.2) +
  geom_text(aes(label = paste0(round(return_rate * 100, 1), "%\n(n=", count, ")"),
                y = return_rate + 0.05), size = 3.5) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 0.8)) +
  labs(
    title = "Client Return Rate by Income Reporting Status",
    subtitle = "Clients who don't report income are much more likely to return",
    x = "Income Status",
    y = "Return Rate",
    caption = "Error bars show standard error"
  ) +
  theme_minimal() +
  theme(legend.position = "none") +
  scale_fill_manual(values = c("Low" = "#E69F00",
                                "Medium" = "#56B4E9",
                                "High" = "#009E73",
                                "Not Reported" = "#CC79A7"))

age_income_summary <- pantry_clean %>%
  group_by(age_group, income_status) %>%
  summarise(
    count = n(),
    return_rate = mean(is_returning),
    .groups = "drop"
  ) %>%
  filter(count > 5) %>%  # Only show groups with enough data
  mutate(income_status = factor(income_status,
                                levels = c("Low", "Medium", "High", "Not Reported")))

ggplot(age_income_summary, aes(x = age_group, y = return_rate, fill = income_status)) +
  geom_col(position = "dodge") +
  geom_text(aes(label = paste0(round(return_rate * 100, 0), "%"),
                group = income_status),
            position = position_dodge(width = 0.9), vjust = -0.5, size = 3) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 0.8)) +
  labs(
    title = "Return Rate by Age Group and Income Status",
    x = "Age Group",
    y = "Return Rate",
    fill = "Income Status"
  ) +
  theme_minimal() +
  scale_fill_manual(values = c("Low" = "#E69F00",
                                "Medium" = "#56B4E9",
                                "High" = "#009E73",
                                "Not Reported" = "#CC79A7"))

ggplot(pantry_clean, aes(x = factor(is_returning), y = household_size, fill = factor(is_returning))) +
  geom_boxplot() +
  geom_jitter(alpha = 0.2, width = 0.2) +
  scale_x_discrete(labels = c("0" = "New Clients", "1" = "Returning Clients")) +
  labs(
    title = "Family Size Distribution: New vs Returning Clients",
    x = "",
    y = "Household Size",
    fill = "Client Type"
  ) +
  theme_minimal() +
  scale_fill_manual(values = c("0" = "#E69F00", "1" = "#56B4E9"),
                     labels = c("New", "Returning")) +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 4, color = "black")

# Create contingency table
income_return_table <- table(pantry_clean$income_status, pantry_clean$is_returning)
colnames(income_return_table) <- c("New", "Returning")

# Convert to proportions for mosaic
mosaicplot(income_return_table,
           main = "Income Status vs Return Status",
           xlab = "Income Status",
           ylab = "Return Status",
           color = c("#E69F00", "#56B4E9"),
           cex.axis = 0.8)

ggplot(pantry_clean, aes(x = household_size, fill = factor(is_returning))) +
  geom_histogram(binwidth = 1, position = "dodge", alpha = 0.7) +
  facet_wrap(~income_status) +
  scale_fill_manual(values = c("0" = "#E69F00", "1" = "#56B4E9"),
                    labels = c("New", "Returning")) +
  labs(
    title = "Family Size Distribution by Income Status",
    x = "Household Size",
    y = "Count",
    fill = "Client Type"
  ) +
  theme_minimal()

# Create a simple dot plot highlighting the main finding
key_finding <- data.frame(
  category = c("Reported Income", "Did Not Report Income"),
  return_rate = c(
    mean(pantry_clean$is_returning[pantry_clean$income_status != "Not Reported"]),
    mean(pantry_clean$is_returning[pantry_clean$income_status == "Not Reported"])
  ),
  count = c(
    sum(pantry_clean$income_status != "Not Reported"),
    sum(pantry_clean$income_status == "Not Reported")
  )
)

ggplot(key_finding, aes(x = category, y = return_rate, color = category)) +
  geom_point(size = 8) +
  geom_segment(aes(x = category, xend = category, y = 0, yend = return_rate),
               linetype = "dashed", alpha = 0.5) +
  geom_text(aes(label = paste0(round(return_rate * 100, 1), "%\n(n=", count, ")")),
            vjust = -1.5, size = 4, color = "black") +
  scale_y_continuous(labels = scales::percent, limits = c(0, 0.7)) +
  labs(
    title = "Income Disclosure and Return Rates",
    subtitle = "Clients who don't report income return at 3x the rate",
    x = "",
    y = "Return Rate",
    caption = "This may indicate established clients are comfortable skipping questions"
  ) +
  theme_minimal() +
  theme(legend.position = "none") +
  scale_color_manual(values = c("Reported Income" = "#E69F00",
                                 "Did Not Report Income" = "#CC79A7"))

# Create multiple plots
p1 <- ggplot(pantry_clean, aes(x = age_group, fill = factor(is_returning))) +
  geom_bar(position = "fill") +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Return Rate by Age", x = "", y = "Proportion", fill = "Returning") +
  scale_fill_manual(values = c("#E69F00", "#56B4E9"))

p2 <- ggplot(pantry_clean, aes(x = factor(has_pets), fill = factor(is_returning))) +
  geom_bar(position = "fill") +
  scale_x_discrete(labels = c("No Pets", "Has Pets")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Return Rate by Pet Ownership", x = "", y = "Proportion", fill = "Returning") +
  scale_fill_manual(values = c("#E69F00", "#56B4E9"))

p3 <- ggplot(pantry_clean, aes(x = household_size, fill = factor(is_returning))) +
  geom_density(alpha = 0.5) +
  labs(title = "Family Size Distribution", x = "Household Size", y = "Density", fill = "Returning") +
  scale_fill_manual(values = c("#E69F00", "#56B4E9"))

# Arrange in grid
grid.arrange(p1, p2, p3, ncol = 2,
             top = "Client Return Patterns: Multiple Factors")