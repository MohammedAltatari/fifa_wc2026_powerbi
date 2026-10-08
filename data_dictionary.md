# FIFA World Cup 2026 – Player Performance: Data Dictionary & Profile

- File: fifa_world_cup_2026_player_performance.csv (~17 MB)
- Rows: 54,600 (grain = one player in one match)
- Columns: 75
- Players: 1,248 | Teams: 48 | Matches: 1,050 | Stadiums: 16
- Dates: 2026-06-11 to 2026-07-31
- Missing values: none
- Each match has 52 rows (26 players per team, 2 teams)

**Important:** this is a SIMULATED dataset (1,050 matches vs 104 in the real tournament; generated player names). Label it "Simulated data" in the portfolio.

## Columns

| Column | Type | Distinct | Example / Range |
|---|---|---|---|
| player_id | text | 1,248 | P00937, P00946, P00957 |
| player_name | text | 1,245 | Pierre-Emile Christensen, Kalidou Mendy, Hee-chan Hwang |
| age | number | 23 | 17 – 39 (avg 26.30) |
| nationality | text | 48 | Qatari, Jamaican, Moroccan |
| team | text | 48 | Qatar, Jamaica, Morocco |
| jersey_number | number | 26 | 1 – 26 (avg 13.50) |
| position | text | 4 | Defender, Midfielder, Forward |
| height_cm | number | 37 | 163 – 200 (avg 181.65) |
| weight_kg | number | 22 | 65 – 87 (avg 75.75) |
| preferred_foot | text | 2 | Right, Left |
| club_name | text | 122 | Gor Mahia, TP Mazembe, Al-Masry |
| market_value_eur | number | 1,246 | 528822 – 2e+08 (avg 20084451.76) |
| match_id | text | 1,050 | M00001, M00002, M00003 |
| match_date | text | 51 | 2026-06-30, 2026-07-28, 2026-06-20 |
| stadium | text | 16 | Lincoln Financial Field, Estadio BBVA, Estadio Akron |
| city | text | 16 | Philadelphia, Monterrey, Guadalajara |
| opponent_team | text | 48 | Qatar, Jamaica, Morocco |
| tournament_stage | text | 7 | Group Stage, Round of 32, Round of 16 |
| match_result | text | 3 | W, L, D |
| goals_team | number | 8 | 0 – 7 (avg 1.33) |
| goals_opponent | number | 8 | 0 – 7 (avg 1.33) |
| minutes_played | number | 87 | 0 – 90 (avg 36.20) |
| goals | number | 5 | 0 – 4 (avg 0.06) |
| assists | number | 4 | 0 – 3 (avg 0.05) |
| shots | number | 12 | 0 – 11 (avg 0.45) |
| shots_on_target | number | 6 | 0 – 5 (avg 0.05) |
| expected_goals_xg | number | 133 | 0 – 2.31 (avg 0.02) |
| expected_assists_xa | number | 130 | 0 – 2.2 (avg 0.02) |
| key_passes | number | 9 | 0 – 8 (avg 0.47) |
| successful_passes | number | 97 | 0 – 97 (avg 15.47) |
| total_passes | number | 101 | 0 – 100 (avg 19.18) |
| pass_accuracy | number | 53 | 0.42 – 0.97 (avg 0.81) |
| dribbles_attempted | number | 11 | 0 – 10 (avg 0.60) |
| successful_dribbles | number | 7 | 0 – 6 (avg 0.16) |
| crosses | number | 9 | 0 – 8 (avg 0.45) |
| successful_crosses | number | 3 | 0 – 2 (avg 0.02) |
| tackles | number | 9 | 0 – 8 (avg 0.80) |
| interceptions | number | 8 | 0 – 7 (avg 0.63) |
| clearances | number | 13 | 0 – 12 (avg 0.81) |
| blocks | number | 5 | 0 – 4 (avg 0.23) |
| aerial_duels_won | number | 8 | 0 – 7 (avg 0.75) |
| aerial_duels_lost | number | 6 | 0 – 5 (avg 0.36) |
| recoveries | number | 13 | 0 – 12 (avg 1.39) |
| defensive_actions | number | 24 | 0 – 23 (avg 2.47) |
| fouls_committed | number | 6 | 0 – 5 (avg 0.42) |
| fouls_suffered | number | 5 | 0 – 4 (avg 0.32) |
| yellow_cards | number | 2 | 0 – 1 (avg 0.10) |
| red_cards | number | 2 | 0 – 1 (avg 0.01) |
| offsides | number | 5 | 0 – 4 (avg 0.09) |
| saves | number | 11 | 0 – 11 (avg 0.12) |
| save_percentage | number | 61 | 0 – 1 (avg 0.03) |
| punches | number | 4 | 0 – 3 (avg 0.03) |
| clean_sheet | number | 2 | 0 – 1 (avg 0.01) |
| goals_conceded | number | 8 | 0 – 7 (avg 0.05) |
| penalty_saves | number | 2 | 0 – 1 (avg 0.00) |
| distance_covered_km | number | 122 | 0 – 14 (avg 4.00) |
| sprint_distance_km | number | 19 | 0 – 2 (avg 0.46) |
| top_speed_kmh | number | 112 | 0 – 37 (avg 18.65) |
| accelerations | number | 45 | 0 – 44 (avg 10.04) |
| decelerations | number | 41 | 0 – 40 (avg 8.85) |
| stamina_score | number | 491 | 50 – 99 (avg 81.89) |
| player_rating | number | 58 | 0 – 9.4 (avg 3.63) |
| performance_score | number | 639 | 0 – 97.7 (avg 36.83) |
| offensive_contribution | number | 981 | 1 – 99 (avg 44.72) |
| defensive_contribution | number | 941 | 5 – 99 (avg 52.73) |
| possession_impact | number | 308 | 0 – 37 (avg 2.85) |
| pressure_resistance | number | 815 | 15 – 99 (avg 60.32) |
| creativity_score | number | 941 | 5 – 99 (avg 46.14) |
| consistency_score | number | 738 | 25 – 99 (avg 63.75) |
| clutch_performance_score | number | 829 | 15 – 99 (avg 55.57) |
| total_goals_tournament | number | 11 | 0 – 10 (avg 0.64) |
| total_assists_tournament | number | 9 | 0 – 8 (avg 0.61) |
| total_minutes_tournament | number | 586 | 0 – 615 (avg 272.30) |
| player_of_match_awards | number | 5 | 0 – 4 (avg 0.03) |
| tournament_rating | number | 63 | 0 – 9.5 (avg 3.63) |

## Category values

- **tournament_stage**: Group Stage (30,056), Round of 32 (9,256), Round of 16 (6,552), Quarter Finals (4,368), Semi Finals (2,184), Third Place Match (1,092), Final (1,092)
- **position**: Defender (18,900), Midfielder (16,800), Forward (12,600), Goalkeeper (6,300)
- **match_result**: W (20,124), L (20,124), D (14,352)
- **preferred_foot**: Right (40,656), Left (13,944)