# RubberRoad Radials - Chaotic Tire Production Scheduling

## Production Lines (A, B, C, D, E)
Each line has different production rates (tires per hour) for each type:

| Line | Standard | Performance | All-Terrain | Winter | Run-Flat |
|------|----------|-------------|-------------|--------|----------|
| A    | 50       | 45          | 40          | 35     | 30       |
| B    | 48       | 52          | 38          | 33     | 28       |
| C    | 55       | 40          | 50          | 30     | 25       |
| D    | 45       | 50          | 45          | 40     | 35       |
| E    | 40       | 48          | 55          | 38     | 32       |

## Time Constraints (all times approximate)
- Cleaning between tire types: 45-75 minutes
- Daily maintenance: 90-150 minutes per line
- Weekly deep cleaning: 4-6 hours per line (must be done once a week)

## Weekly Quotas (must be met within ±5%)
- Standard: 12000-13000 tires
- Performance: 9000-10000 tires
- All-Terrain: 7000-8000 tires
- Winter: 5000-6000 tires
- Run-Flat: 4000-5000 tires

## Additional Constraints and Quirks
- Factory operates 24/6 (closed on Sundays for main power grid maintenance)
- Line A can only produce Standard and Performance tires
- Line C experiences 10-20% efficiency drop every third day due to local power fluctuations
- Run-Flat tires can only be produced between 10 PM and 6 AM due to noise regulations
- Raw material deliveries are unpredictable, arriving 1-3 times per week at random times
- Each production run should be at least 3 hours, but not exceed 8 hours
- Workers prefer not to change tire types more than twice per shift

## Staffing Issues
- Three 8-hour shifts per day
- 20% of staff are trainees (15% less efficient)
- 10% chance of understaffing on any given shift (10% productivity decrease)
- Union mandated breaks: 2 x 15 min, 1 x 30 min per shift (staggered, but may impact production)

## Quality Control
- 1-3% of tires fail inspection and must be scrapped
- Every 1000th tire undergoes extensive testing, halting its production line for 20-40 minutes

## Unexpected Events (must be factored into scheduling)
- One 6-8 hour complete factory shutdown for emergency repairs (day and time unknown)
- Two 2-3 hour surprise safety drills (days and times unknown)
- One week of heatwave reducing overall efficiency by 5-15% (exact impact varies daily)

## Market Demands
- 30% surge in Winter tire orders if temperature drops below freezing
- 25% increase in All-Terrain tire demand during local off-road racing event (dates TBA)
- Potential rush order of 2000 Performance tires (50% chance, 3-day notice if it happens)

## Objective
Maximize total tire production while meeting all quotas and constraints over a 4-week period. Minimize overtime and waste. Adapt to unexpected events and market changes.

## Additional Considerations
- Energy costs are 20% higher during peak hours (9 AM - 5 PM)
- Storage capacity is limited to 3 days' worth of production
- Some tire compounds degrade if not used within 5 days of mixing
- Local environmental regulations limit certain production processes during daytime hours