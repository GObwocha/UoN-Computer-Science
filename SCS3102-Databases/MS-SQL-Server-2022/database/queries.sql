CREATE DATABASE KenyaEnvironmentPortalDb;
GO
INSERT INTO dbo.KnowledgeStopWords (Word)
VALUES
(N'a'), (N'an'), (N'and'), (N'are'), (N'as'), (N'at'), (N'be'), (N'by'),
(N'for'), (N'from'), (N'has'), (N'in'), (N'is'), (N'it'), (N'of'), (N'on'),
(N'or'), (N'that'), (N'the'), (N'their'), (N'this'), (N'to'), (N'with');
GO

INSERT INTO dbo.Counties
(
    Name, Region, Headquarters, PopulationEstimate, AreaSqKm,
    EcosystemFocus, RiskLevel, Overview, ContactPhone, ContactEmail
)
VALUES
(N'Mombasa', N'Coast', N'Mombasa', 1208333, 295.0, N'Coastal resilience and marine litter', N'High', N'Priority county for beach sanitation, storm surge resilience and marine litter enforcement around the port zone.', N'+254 700 100 001', N'mombasa@kecsa.go.ke'),
(N'Kwale', N'Coast', N'Kwale', 866820, 8270.3, N'Coastal forests and quarry reclamation', N'Medium', N'Coordinates coastal forest protection, quarry-site rehabilitation and storm-water planning in growing towns.', N'+254 700 100 002', N'kwale@kecsa.go.ke'),
(N'Kilifi', N'Coast', N'Kilifi', 1453787, 12917.5, N'Mangrove regeneration and beach cleanup', N'High', N'Coastal office handles mangrove restoration, marine debris action and tourism-zone shoreline cleanup.', N'+254 700 100 003', N'kilifi@kecsa.go.ke'),
(N'Tana River', N'Coast Hinterland', N'Hola', 315943, 35375.8, N'Delta floodplains and riverine ecosystems', N'High', N'Leads floodplain management, delta ecosystem protection and seasonal river monitoring for vulnerable settlements.', N'+254 700 100 004', N'tanariver@kecsa.go.ke'),
(N'Lamu', N'Coast', N'Lamu', 143920, 6273.1, N'Marine parks and mangrove protection', N'Medium', N'Combines heritage coast management, mangrove care and marine ecosystem monitoring across island and mainland wards.', N'+254 700 100 005', N'lamu@kecsa.go.ke'),
(N'Taita Taveta', N'Coast Hinterland', N'Voi', 340671, 17084.1, N'Catchment rehabilitation and mining oversight', N'Medium', N'Works on catchment recovery, quarry and mining compliance, and wildlife-linked land stewardship.', N'+254 700 100 006', N'taitataveta@kecsa.go.ke'),
(N'Garissa', N'North Eastern', N'Garissa', 835482, 44753.0, N'River Tana catchment and drought response', N'High', N'Coordinates flood preparedness along the Tana corridor while strengthening dryland vegetation recovery inland.', N'+254 700 100 007', N'garissa@kecsa.go.ke'),
(N'Wajir', N'North Eastern', N'Wajir', 781263, 55840.0, N'Borehole governance and dryland recovery', N'High', N'Emphasis is on sustainable borehole use, range reseeding and emergency water-point coordination.', N'+254 700 100 008', N'wajir@kecsa.go.ke'),
(N'Mandera', N'North Eastern', N'Mandera', 867457, 25798.3, N'Cross-border dryland water security', N'High', N'County teams focus on strategic water points, rangeland restoration and drought planning near border settlements.', N'+254 700 100 009', N'mandera@kecsa.go.ke'),
(N'Marsabit', N'Northern Frontier', N'Marsabit', 459785, 66923.0, N'Dryland ecosystems and solid waste', N'Medium', N'County teams combine urban waste management with fragile ecosystem planning across vast arid landscapes.', N'+254 700 100 010', N'marsabit@kecsa.go.ke'),
(N'Isiolo', N'Northern Frontier', N'Isiolo', 268002, 25336.1, N'Watershed management and grazing plans', N'Medium', N'Local office focuses on water points, grazing coordination and erosion control in transport-corridor settlements.', N'+254 700 100 011', N'isiolo@kecsa.go.ke'),
(N'Meru', N'Eastern Highlands', N'Meru', 1545714, 7006.0, N'Highlands soil conservation', N'Medium', N'Runs hillside erosion control and upper catchment protection programs serving tea, coffee and mixed-farming areas.', N'+254 700 100 012', N'meru@kecsa.go.ke'),
(N'Tharaka-Nithi', N'Eastern Highlands', N'Kathwana', 393177, 2564.0, N'Upper catchment farming and forest edges', N'Medium', N'Protects hill catchments, hillside farms and riparian corridors linking upland and lower semi-arid zones.', N'+254 700 100 013', N'tharakanithi@kecsa.go.ke'),
(N'Embu', N'Eastern Highlands', N'Embu', 608599, 2818.0, N'Water tower protection and agroforestry', N'Medium', N'Supports agroforestry, spring protection and compliance monitoring around important water-source landscapes.', N'+254 700 100 014', N'embu@kecsa.go.ke'),
(N'Kitui', N'Lower Eastern', N'Kitui', 1136187, 30496.5, N'Sand dams and semi-arid land restoration', N'Medium', N'Coordinates sand-dam protection, semi-arid land restoration and settlement water planning across large dry zones.', N'+254 700 100 015', N'kitui@kecsa.go.ke'),
(N'Machakos', N'Lower Eastern', N'Machakos', 1421932, 5952.9, N'Sand harvesting control and water pans', N'Medium', N'County office is expanding watershed protection alongside community water pan rehabilitation and quarry oversight.', N'+254 700 100 016', N'machakos@kecsa.go.ke'),
(N'Makueni', N'Lower Eastern', N'Wote', 987653, 8008.9, N'Dryland farming catchments and river protection', N'Medium', N'Builds riverbank protection, water harvesting and low-rainfall land restoration into county service planning.', N'+254 700 100 017', N'makueni@kecsa.go.ke'),
(N'Nyandarua', N'Central', N'Ol Kalou', 638289, 3245.0, N'Moorland water sources and erosion control', N'Medium', N'Protects upper water sources, moorland catchments and hillside soils that feed major downstream rivers.', N'+254 700 100 018', N'nyandarua@kecsa.go.ke'),
(N'Nyeri', N'Central', N'Nyeri', 759164, 3337.1, N'Aberdare catchment protection', N'Medium', N'Focused on forest catchments, clean water sources and land rehabilitation in upper watershed communities.', N'+254 700 100 019', N'nyeri@kecsa.go.ke'),
(N'Kirinyaga', N'Central', N'Kerugoya', 610411, 1478.1, N'Irrigation efficiency and riverbank protection', N'Medium', N'Coordinates irrigation water use, riparian reserve enforcement and smallholder soil conservation in rice-growing zones.', N'+254 700 100 020', N'kirinyaga@kecsa.go.ke'),
(N'Murang''a', N'Central', N'Murang''a', 1056640, 2325.8, N'Upper Tana catchment and solid waste', N'High', N'Combines catchment protection, market-waste controls and river source monitoring for fast-growing towns.', N'+254 700 100 021', N'muranga@kecsa.go.ke'),
(N'Kiambu', N'Central', N'Kiambu', 2417735, 2538.0, N'River rehabilitation and peri-urban waste', N'High', N'Works on riverbank restoration, wastewater compliance and fast-growing peri-urban solid-waste systems.', N'+254 700 100 022', N'kiambu@kecsa.go.ke'),
(N'Turkana', N'North Rift', N'Lodwar', 926976, 68180.0, N'Climate resilience and aquifer protection', N'High', N'Large dryland county prioritizing aquifer governance, solar water systems and drought early-warning coverage.', N'+254 700 100 023', N'turkana@kecsa.go.ke'),
(N'West Pokot', N'North Rift', N'Kapenguria', 621241, 9169.4, N'Hillside restoration and water harvesting', N'Medium', N'County teams support slope stabilization, range recovery and water harvesting in both hills and dry valley zones.', N'+254 700 100 024', N'westpokot@kecsa.go.ke'),
(N'Samburu', N'North Rift', N'Maralal', 310327, 20182.5, N'Rangeland recovery and watershed care', N'Medium', N'Focuses on grazing-land balance, dry-season water security and land-restoration support for pastoral communities.', N'+254 700 100 025', N'samburu@kecsa.go.ke'),
(N'Trans Nzoia', N'North Rift', N'Kitale', 990341, 2469.9, N'Slope stabilization and urban drainage', N'Medium', N'Combines agricultural-runoff controls with drainage improvement in market towns and hillside wards.', N'+254 700 100 026', N'transnzoia@kecsa.go.ke'),
(N'Uasin Gishu', N'North Rift', N'Eldoret', 1163186, 3345.2, N'Urban drainage and agricultural runoff', N'Medium', N'County team manages drainage modernization while reducing runoff and waste pressure from agricultural zones.', N'+254 700 100 027', N'uasingishu@kecsa.go.ke'),
(N'Elgeyo-Marakwet', N'North Rift', N'Iten', 454480, 3029.8, N'Escarpment restoration and spring protection', N'Medium', N'Protects escarpment slopes, spring recharge zones and settlement drainage in highland communities.', N'+254 700 100 028', N'elgeyomarakwet@kecsa.go.ke'),
(N'Nandi', N'North Rift', N'Kapsabet', 885711, 2884.5, N'Watershed farming and river source protection', N'Medium', N'Links tea-growing catchments, river source protection and local waste compliance across high-rainfall wards.', N'+254 700 100 029', N'nandi@kecsa.go.ke'),
(N'Baringo', N'North Rift', N'Kabarnet', 666763, 11015.3, N'Land restoration and water security', N'High', N'County operations target degraded landscapes, water harvesting and settlement resilience in flood-prone valleys.', N'+254 700 100 030', N'baringo@kecsa.go.ke'),
(N'Laikipia', N'Central Rift', N'Rumuruti', 518560, 8696.1, N'Wildlife corridors and drought planning', N'Medium', N'Brings together ranching, wildlife conservancies and county officers on land restoration and drought plans.', N'+254 700 100 031', N'laikipia@kecsa.go.ke'),
(N'Nakuru', N'Rift Valley', N'Nakuru', 2162202, 7509.0, N'Forest recovery and landfill control', N'High', N'Balances urban growth with forest restoration, dumpsite regulation and lake-basin land-use controls.', N'+254 700 100 032', N'nakuru@kecsa.go.ke'),
(N'Narok', N'South Rift', N'Narok', 1157873, 17921.2, N'Mau forest restoration', N'High', N'Concentrates on forest-edge restoration, grassland recovery and tourism-area waste management.', N'+254 700 100 033', N'narok@kecsa.go.ke'),
(N'Kajiado', N'Southern', N'Kajiado', 1117840, 21871.0, N'Rangeland conservation and human-wildlife balance', N'High', N'Prioritizes grazing-land recovery, wildlife corridor protection and drought-sensitive planning near Amboseli ecosystems.', N'+254 700 100 034', N'kajiado@kecsa.go.ke'),
(N'Kericho', N'South Rift', N'Kericho', 901777, 2454.5, N'Tea catchment protection and waste control', N'Medium', N'Protects tea-growing catchments, town drainage and waste controls in fast-growing roadside markets.', N'+254 700 100 035', N'kericho@kecsa.go.ke'),
(N'Bomet', N'South Rift', N'Bomet', 875689, 2037.4, N'Upper Mara catchments and waste management', N'Medium', N'Supports river source protection, farm-runoff reduction and solid-waste systems in upland towns.', N'+254 700 100 036', N'bomet@kecsa.go.ke'),
(N'Kakamega', N'Western', N'Kakamega', 1867579, 3033.8, N'Rainforest conservation and river health', N'Medium', N'Protects forest fragments, urban drainage and river quality while coordinating market-waste interventions.', N'+254 700 100 037', N'kakamega@kecsa.go.ke'),
(N'Vihiga', N'Western', N'Mbale', 590013, 531.0, N'Hillside drainage and market sanitation', N'Medium', N'County staff address steep-slope drainage, market sanitation and stream-bank encroachment in dense settlements.', N'+254 700 100 038', N'vihiga@kecsa.go.ke'),
(N'Bungoma', N'Western', N'Bungoma', 1670570, 3023.9, N'Slope stabilization and market waste', N'Medium', N'Runs hillside rehabilitation, drainage works and town-market waste management upgrades.', N'+254 700 100 039', N'bungoma@kecsa.go.ke'),
(N'Busia', N'Western', N'Busia', 893681, 1628.4, N'Border waste management and wetland care', N'Medium', N'County strategy centers on border-town waste systems, wetland protection and public sanitation improvements.', N'+254 700 100 040', N'busia@kecsa.go.ke'),
(N'Siaya', N'Lake Basin', N'Siaya', 993183, 2496.1, N'Lake basin sanitation', N'Medium', N'Improves shoreline sanitation, fish-landing waste control and small-town water quality monitoring.', N'+254 700 100 041', N'siaya@kecsa.go.ke'),
(N'Kisumu', N'Lake Basin', N'Kisumu', 1155574, 2085.9, N'Lake restoration and wetland protection', N'High', N'Coordinates wetland mapping, shoreline sanitation and fisheries catchment protection around Lake Victoria.', N'+254 700 100 042', N'kisumu@kecsa.go.ke'),
(N'Homa Bay', N'Lake Basin', N'Homa Bay', 1131950, 3154.7, N'Shoreline sanitation and fish landing waste', N'Medium', N'County operations improve landing-site sanitation, bay cleanups and wetland protection around lake-edge communities.', N'+254 700 100 043', N'homabay@kecsa.go.ke'),
(N'Migori', N'Lake Basin', N'Migori', 1116436, 2586.4, N'River catchments and small-scale mining control', N'Medium', N'Combines river source care, drainage monitoring and mining-site rehabilitation in mixed rural and town settings.', N'+254 700 100 044', N'migori@kecsa.go.ke'),
(N'Kisii', N'Lake Basin', N'Kisii', 1266860, 1317.5, N'Hill slope drainage and urban waste', N'Medium', N'Protects steep urban catchments, drainage channels and river quality in dense highland settlements.', N'+254 700 100 045', N'kisii@kecsa.go.ke'),
(N'Nyamira', N'Lake Basin', N'Nyamira', 605576, 899.4, N'Tea-zone river protection and drainage', N'Medium', N'Focuses on hill catchments, town drainage and stream-bank protection in tea and banana zones.', N'+254 700 100 046', N'nyamira@kecsa.go.ke'),
(N'Nairobi City', N'Central Metro', N'Nairobi', 4397073, 696.1, N'Urban drainage and air quality', N'High', N'Focuses on river cleanup, air quality monitoring and storm-water management around dense urban neighborhoods.', N'+254 700 100 047', N'nairobi@kecsa.go.ke');
GO

INSERT INTO dbo.ResponseLocations
(
    LocationName,
    LocationType,
    CountyId,
    Headquarters,
    FocusArea,
    ContactPhone,
    ContactEmail
)
SELECT
    c.Name + N' County Environment Office',
    N'County Office',
    c.CountyId,
    c.Headquarters,
    c.EcosystemFocus,
    c.ContactPhone,
    c.ContactEmail
FROM dbo.Counties c;
GO

INSERT INTO dbo.ResponseLocations
(
    LocationName,
    LocationType,
    CountyId,
    Headquarters,
    FocusArea,
    ContactPhone,
    ContactEmail
)
VALUES
(N'National Disaster Coordination Centre', N'National Coordination', NULL, N'Nairobi', N'Inter-county disaster alerts, flood response and emergency coordination', N'+254 800 111 999', N'disasterdesk@kecsa.go.ke');
GO

INSERT INTO dbo.Services (Title, Description, Controller, Action, SearchTerm, SortOrder)
VALUES
(N'Browse county offices', N'View all 47 counties, their ecosystem focus areas and county office profiles.', N'Counties', N'Index', NULL, 1),
(N'Check licensing services', N'Review environmental permits, requirements, fees and processing windows.', N'Licensing', N'Index', NULL, 2),
(N'Apply for a licence', N'Submit an online licensing request for review by the relevant office.', N'LicenseApplications', N'Create', NULL, 3),
(N'Explore research activities', N'View field studies, monitoring work and county-linked environmental investigations.', N'Research', N'Index', NULL, 4),
(N'Search records and guidance', N'Search published county records, licensing information, research activity and notices.', N'KnowledgeSearch', N'Index', NULL, 5),
(N'Report an incident', N'Submit a pollution, flood or disaster report for review by the responsible office.', N'IncidentDesk', N'Index', NULL, 6),
(N'National disaster coordination desk', N'Use the national disaster coordination location for cross-county emergencies and public alerts.', N'IncidentDesk', N'Index', NULL, 7),
(N'Using this portal', N'Find service information, county contacts, applications and records from one public portal.', N'Home', N'Database', NULL, 8),
(N'Find coast counties', N'Jump straight to counties with coastal resilience and marine management programs.', N'Counties', N'Index', N'Coast', 9),
(N'Check northern drought areas', N'Filter counties that are commonly associated with dryland planning and water security.', N'Counties', N'Index', N'North', 10),
(N'Explore forest counties', N'Search counties where watershed or forest rehabilitation is a major priority.', N'Counties', N'Index', N'forest', 11);
GO

INSERT INTO dbo.AdminUsers
(
    FullName,
    Username,
    Email,
    PasswordHash,
    RoleName,
    IsActive
)
VALUES
(
    N'System Administrator',
    N'admin',
    N'admin@kecsa.go.ke',
    N'scrypt:32768:8:1$cQvOZxDqWqlnfVcR$e15db87f4bd26c4d1bc627c57468e63147ce3a1e7f384745cdf62181625c840c84f1dabbe42b45fb49674a231deb4826f269509ae8c402e8c8def4f8a54bb469',
    N'Super Administrator',
    1
);
GO

INSERT INTO dbo.LicensingServices
(
    CountyId,
    Title,
    Category,
    ProcessingWindowDays,
    FeeKsh,
    AppliesTo,
    Summary,
    Requirements,
    IsFeatured,
    SortOrder
)
VALUES
(NULL, N'Environmental impact assessment licence', N'Impact assessment', 30, 25000, N'Large infrastructure, industrial, road and quarry projects', N'Used for projects that require structured environmental review before implementation.', N'Application form, project brief, site coordinates and proponent identification.', 1, 1),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Nairobi City'), N'Air emissions operating permit', N'Air quality compliance', 21, 18500, N'Factories, boilers, generators and high-emission facilities', N'Supports county and national review of controlled emissions from urban and industrial sites.', N'Emission control plan, equipment inventory and latest compliance inspection notes.', 1, 2),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kisumu'), N'Wetland activity permit', N'Wetland protection', 18, 12000, N'Landing sites, shoreline works and wetland-adjacent community projects', N'Controls activity near wetlands to protect buffers, drainage and ecological function.', N'Site sketch, wetland buffer statement and community endorsement letter.', 1, 3),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Mombasa'), N'Coastal event and beach use permit', N'Coastal management', 14, 9000, N'Large public events, temporary beach structures and shoreline activations', N'Helps coastal offices regulate public use of sensitive shoreline and marine-adjacent spaces.', N'Event schedule, sanitation plan and waste collection arrangement.', 1, 4),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Taita Taveta'), N'Quarry rehabilitation compliance review', N'Extraction compliance', 24, 16000, N'Quarries, mining support yards and restoration contractors', N'Checks rehabilitation plans for extraction sites and nearby riverbank recovery commitments.', N'Site rehabilitation plan, extraction map and restoration timeline.', 0, 5),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Machakos'), N'Sand harvesting environmental approval', N'River resource management', 16, 11000, N'Sand harvesting groups and riverbed extraction operators', N'Screens riverbed extraction activity and transport staging areas against catchment protection rules.', N'Sand harvesting plan, extraction route and community oversight committee details.', 0, 6),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Turkana'), N'Borehole environmental screening permit', N'Water resource screening', 20, 14500, N'Public boreholes, strategic water points and solar pumping sites', N'Ensures new or upgraded boreholes account for environmental risk, waste handling and recharge protection.', N'Hydrogeology note, borehole coordinates and waste management plan.', 0, 7),
(NULL, N'Community tree nursery registration', N'Ecosystem restoration', 10, 3000, N'Schools, youth groups and registered community organizations', N'Registers tree nursery operators supporting county restoration campaigns and school greening projects.', N'Registration certificate, site contact and seedling management plan.', 0, 8);
GO

INSERT INTO dbo.ResearchActivities
(
    CountyId,
    Title,
    ResearchTheme,
    Status,
    LeadOffice,
    StartDate,
    Summary,
    Outputs,
    IsFeatured
)
VALUES
(NULL, N'National environmental data observatory baseline', N'Data systems', N'Active', N'National Planning and Analytics Unit', '2026-03-01', N'Builds a baseline dataset combining county environmental indicators, incident trends and permit activity for agency planning.', N'Baseline dashboard and county indicator matrix', 1),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Nairobi City'), N'Nairobi industrial river discharge audit', N'Water quality', N'Field analysis', N'Nairobi City water quality laboratory', '2026-03-18', N'Inspectors and lab teams are mapping discharge points and sampling river segments affected by industrial runoff.', N'Sampling log and discharge hotspot map', 1),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kilifi'), N'Mangrove regeneration survival study', N'Coastal ecosystems', N'Active', N'Kilifi coastal restoration desk', '2026-03-14', N'Tracks seedling survival, tidal disturbance and community stewardship outcomes across restoration plots.', N'Survival scorecards and nursery lessons report', 1),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Narok'), N'Mau forest edge soil loss survey', N'Catchment restoration', N'Active', N'Narok forest recovery unit', '2026-03-10', N'Field teams are measuring slope erosion and land-use pressure in settlements along sensitive forest-edge zones.', N'Erosion transects and village risk profile', 1),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Turkana'), N'Dryland borehole resilience mapping', N'Drought resilience', N'Monitoring', N'Turkana dryland planning office', '2026-03-08', N'County teams are comparing borehole downtime, water demand and maintenance patterns in priority dry-season corridors.', N'Water-point uptime map and vulnerability brief', 0),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kisumu'), N'Lake Victoria shoreline wetland survey', N'Wetland monitoring', N'Published', N'Kisumu wetland and shoreline unit', '2026-03-04', N'Shoreline teams completed wetland mapping and sanitation observations around major landing and settlement areas.', N'Wetland atlas summary and sanitation gap list', 0),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Tana River'), N'Tana delta floodplain habitat mapping', N'Floodplain ecology', N'Active', N'Tana River ecosystem office', '2026-02-26', N'Combines flood history, settlement exposure and habitat condition data to support floodplain protection planning.', N'Floodplain habitat map and settlement exposure notes', 0),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kakamega'), N'Kakamega school biodiversity field study', N'Forest biodiversity', N'Scheduled', N'Kakamega county education and forest liaison desk', '2026-04-03', N'School clubs and county officers will conduct guided biodiversity observations in buffer sites linked to restoration work.', N'Field workbook and school biodiversity checklist', 0);
GO

INSERT INTO dbo.Updates (CountyId, Title, Summary, PublishDate, Category, IsFeatured)
VALUES
(NULL, N'National disaster coordination centre activates flood and drought watch desk', N'County officers have been asked to feed incident data to the national coordination desk for cross-county flood and drought monitoring.', '2026-03-26', N'Alert', 1),
(NULL, N'National drought readiness bulletin released for county planners', N'County officers have been asked to review water storage, borehole governance and dry-season response plans before the next quarter.', '2026-03-24', N'Guidance', 1),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Nairobi City'), N'Nairobi River cleanup phase one begins in industrial sections', N'Joint teams are piloting litter traps, water sampling and enforcement patrols along priority river segments.', '2026-03-22', N'Press release', 1),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kilifi'), N'Kilifi school partnership expands mangrove seedling nurseries', N'Environmental clubs and ward offices are scaling up community mangrove nurseries ahead of the long-rains planting window.', '2026-03-20', N'News', 0),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Turkana'), N'Turkana approves phase two of solar borehole rehabilitation', N'County planners extended the rehabilitation package to additional dry-season access points.', '2026-03-18', N'Project update', 0),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kakamega'), N'Kakamega forest buffer survey opens for public participation', N'Communities bordering key forest sections have been invited to verify mapping outputs and local restoration priorities.', '2026-03-16', N'Consultation', 0),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Mombasa'), N'Mombasa marine litter taskforce launches beach and harbor cleanout', N'County and port partners will track marine litter hotspots and intensify shoreline cleanup days.', '2026-03-14', N'Press release', 0),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Narok'), N'Narok expands ranger-supported restoration around Mau fringe villages', N'Community groups will receive seedlings, fencing support and monitoring tools in sensitive catchment areas.', '2026-03-11', N'News', 0),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kisumu'), N'Kisumu publishes wetland mapping summary for priority landing sites', N'The new summary identifies shoreline sanitation gaps and areas needing buffer restoration.', '2026-03-09', N'Research', 0),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Homa Bay'), N'Homa Bay expands fish-landing sanitation support', N'County officers will roll out new waste sorting and shoreline cleanup routines at selected landing sites.', '2026-03-08', N'Project update', 0);
GO

INSERT INTO dbo.Programs (CountyId, Title, Status, BudgetMillions, Beneficiaries, Summary)
VALUES
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Nairobi City'), N'Urban River Recovery Corridors', N'Active', 148.5, 235000, N'Combines riverbank cleanup, storm-water interceptors and neighborhood awareness campaigns in dense settlement areas.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Mombasa'), N'Coastal Solid Waste Interception Network', N'Active', 96.0, 180000, N'Expands litter interception, segregation points and marine debris monitoring around beaches and the port.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kisumu'), N'Lake Edge Wetland Restoration', N'Active', 84.2, 142000, N'Protects papyrus wetlands, landing sites and shoreline sanitation zones around peri-urban settlements.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Nakuru'), N'Menengai Catchment and Dumpsite Upgrade', N'Planned', 121.0, 210000, N'Links waste-cell upgrades with upper catchment restoration and drainage redesign in growth corridors.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kiambu'), N'Peri-Urban Waste Compliance Drive', N'Active', 77.4, 165000, N'Improves waste transfer controls, riparian monitoring and sewer overflow response in satellite towns.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kajiado'), N'Amboseli Rangeland Water Balance Program', N'Active', 111.8, 98000, N'Coordinates water points, grazing plans and ecosystem monitoring for wildlife-compatible dryland management.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Narok'), N'Mau Forest Community Restoration Blocks', N'Active', 102.3, 86000, N'Funds seedlings, boundary support and community restoration teams across the forest fringe.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Turkana'), N'Solar Borehole Reliability Upgrade', N'Active', 134.6, 124000, N'Improves solar pumping systems, source protection and telemetry at strategic water points.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kakamega'), N'Rainforest Buffer Livelihood Program', N'Planned', 69.5, 54000, N'Pairs forest-edge agroforestry with drainage controls and household tree planting.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kilifi'), N'Mangrove and Beach Stewardship Scheme', N'Active', 88.1, 73000, N'Community groups manage mangrove nurseries, shoreline cleanup and erosion watch activities.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Taita Taveta'), N'Quarry Compliance and Riverbank Recovery', N'Monitoring', 45.0, 31000, N'Inspects extraction sites while restoring adjacent riverbanks and access roads.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Uasin Gishu'), N'Urban Drainage and Farm Runoff Shield', N'Planned', 72.2, 91000, N'Improves storm-water channels and demonstration runoff-control plots near growth centers.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Homa Bay'), N'Lake Shore Waste Transfer Improvement', N'Active', 54.3, 47000, N'Builds waste transfer points and shoreline collection systems around busy lake landing areas.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Kericho'), N'Tea Catchment Springs Protection Program', N'Planned', 41.8, 38000, N'Protects spring heads, tea-zone drains and small river source points serving rural communities.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Mandera'), N'Dryland Water Access Resilience Scheme', N'Active', 118.7, 82000, N'Strengthens emergency water points, catchment fencing and public reporting for drought-sensitive settlements.'),
((SELECT CountyId FROM dbo.Counties WHERE Name = N'Vihiga'), N'Town Drainage and Market Sanitation Upgrade', N'Monitoring', 28.4, 26000, N'Improves drainage chokepoints and sanitation routines in densely settled market centers.');
GO

INSERT INTO dbo.LicenseApplications
(
    LicenseServiceId,
    ProjectCountyId,
    ApplicantName,
    ApplicantEmail,
    OrganizationName,
    ProjectLocation,
    ProjectSummary,
    SupportingDocuments,
    Status,
    SubmittedAt
)
VALUES
(
    (SELECT LicenseServiceId FROM dbo.LicensingServices WHERE Title = N'Environmental impact assessment licence'),
    (SELECT CountyId FROM dbo.Counties WHERE Name = N'Nairobi City'),
    N'Grace Njeri',
    N'grace.njeri@example.com',
    N'CityGreen Infrastructure Ltd',
    N'Industrial Area, Nairobi',
    N'Application for environmental review of a medium-scale recycling and materials recovery site planned near existing industrial utilities.',
    N'Project brief, site map, company certificate and sanitation concept note',
    N'Submitted',
    DATEADD(DAY, -3, SYSDATETIME())
),
(
    (SELECT LicenseServiceId FROM dbo.LicensingServices WHERE Title = N'Wetland activity permit'),
    (SELECT CountyId FROM dbo.Counties WHERE Name = N'Kisumu'),
    N'Brian Odhiambo',
    N'brian.odhiambo@example.com',
    N'Lakefront Community Initiative',
    N'Dunga shoreline, Kisumu',
    N'Community group seeking approval for a controlled boardwalk and cleanup staging zone near a sensitive wetland edge.',
    N'Community endorsement letter, wetland buffer sketch and site photos',
    N'Under review',
    DATEADD(DAY, -1, SYSDATETIME())
);
GO

INSERT INTO dbo.IncidentReports
(
    ReporterName,
    ReporterEmail,
    CountyId,
    ResponseLocationId,
    Category,
    Location,
    Description,
    Status,
    ReportedAt
)
VALUES
(N'Faith Mwangi', N'faith.mwangi@example.com',
 (SELECT CountyId FROM dbo.Counties WHERE Name = N'Nairobi City'),
 (SELECT ResponseLocationId FROM dbo.ResponseLocations WHERE LocationName = N'Nairobi City County Environment Office'),
 N'Illegal dumping', N'Korogocho bridge', N'Unsorted waste has been dumped close to the riverbank for three days and is blocking storm-water flow.', N'Under review', DATEADD(DAY, -4, SYSDATETIME())),
(N'Abdi Hassan', N'abdi.hassan@example.com',
 (SELECT CountyId FROM dbo.Counties WHERE Name = N'Garissa'),
 (SELECT ResponseLocationId FROM dbo.ResponseLocations WHERE LocationName = N'Garissa County Environment Office'),
 N'Flood risk', N'Tana embankment section B', N'Erosion near the embankment has widened after recent rains and nearby farms are at risk if the bank fails.', N'New', DATEADD(DAY, -2, SYSDATETIME())),
(N'Joy Achieng', N'joy.achieng@example.com',
 (SELECT CountyId FROM dbo.Counties WHERE Name = N'Kisumu'),
 (SELECT ResponseLocationId FROM dbo.ResponseLocations WHERE LocationName = N'Kisumu County Environment Office'),
 N'Water contamination', N'Dunga landing site', N'Fish traders reported dirty discharge entering the lake edge and causing a strong smell in the morning.', N'Closed', DATEADD(DAY, -1, SYSDATETIME())),
(N'Peter Wekesa', N'peter.wekesa@example.com',
 NULL,
 (SELECT ResponseLocationId FROM dbo.ResponseLocations WHERE LocationName = N'National Disaster Coordination Centre'),
 N'Disaster response', N'National flood desk, Nairobi', N'Two counties reported flood displacement overnight and the national centre opened a cross-county coordination ticket for rapid response.', N'Escalated', DATEADD(HOUR, -10, SYSDATETIME()));
GO

EXEC dbo.RebuildKnowledgeIndex;
GO

DECLARE @BaseFolder NVARCHAR(500) = 'C:\ProjectBackups\';
DECLARE @BackupPath NVARCHAR(500);
DECLARE @BackupCommand NVARCHAR(MAX);
DECLARE @FileName NVARCHAR(100) = 'KenyaEnvironmentPortal_DynamicBackup.bak';
EXEC master.dbo.xp_create_subdir @BaseFolder;
SET @BackupPath = @BaseFolder + @FileName;
SET @BackupCommand = 'BACKUP DATABASE KenyaEnvironmentPortalDb TO DISK = ''' + @BackupPath + ''' WITH FORMAT, INIT;';
EXEC sp_executesql @BackupCommand;
SELECT 'Backup successfully created at: ' + @BackupPath AS BackupStatus;