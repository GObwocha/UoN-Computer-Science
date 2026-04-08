CREATE DATABASE KenyaEnvironmentPortalDb;
GO
CREATE TABLE dbo.Counties
(
    CountyId INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL UNIQUE,
    Region NVARCHAR(80) NOT NULL,
    Headquarters NVARCHAR(80) NOT NULL,
    PopulationEstimate INT NOT NULL,
    AreaSqKm DECIMAL(10,1) NOT NULL,
    EcosystemFocus NVARCHAR(120) NOT NULL,
    RiskLevel NVARCHAR(20) NOT NULL,
    Overview NVARCHAR(500) NOT NULL,
    ContactPhone NVARCHAR(40) NOT NULL,
    ContactEmail NVARCHAR(120) NOT NULL
);
GO

CREATE TABLE dbo.ResponseLocations
(
    ResponseLocationId INT IDENTITY(1,1) PRIMARY KEY,
    LocationName NVARCHAR(140) NOT NULL,
    LocationType NVARCHAR(60) NOT NULL,
    CountyId INT NULL FOREIGN KEY REFERENCES dbo.Counties(CountyId),
    Headquarters NVARCHAR(80) NOT NULL,
    FocusArea NVARCHAR(180) NOT NULL,
    ContactPhone NVARCHAR(40) NOT NULL,
    ContactEmail NVARCHAR(120) NOT NULL
);
GO

CREATE TABLE dbo.Services
(
    ServiceId INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(120) NOT NULL,
    Description NVARCHAR(280) NOT NULL,
    Controller NVARCHAR(60) NOT NULL,
    Action NVARCHAR(60) NOT NULL,
    SearchTerm NVARCHAR(100) NULL,
    SortOrder INT NOT NULL
);
GO

CREATE TABLE dbo.AdminUsers
(
    AdminUserId INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(120) NOT NULL,
    Username NVARCHAR(60) NOT NULL UNIQUE,
    Email NVARCHAR(120) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    RoleName NVARCHAR(60) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    LastLoginAt DATETIME2 NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    SystemUser NVARCHAR(50)
);
GO

CREATE TABLE dbo.AdminActivityLog
(
    ActivityLogId INT IDENTITY(1,1) PRIMARY KEY,
    AdminUserId INT NOT NULL FOREIGN KEY REFERENCES dbo.AdminUsers(AdminUserId),
    ActivityType NVARCHAR(80) NOT NULL,
    EntityType NVARCHAR(80) NOT NULL,
    EntityId INT NULL,
    OccurredAt DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

CREATE TABLE dbo.LicensingServices
(
    LicenseServiceId INT IDENTITY(1,1) PRIMARY KEY,
    CountyId INT NULL FOREIGN KEY REFERENCES dbo.Counties(CountyId),
    Title NVARCHAR(160) NOT NULL,
    Category NVARCHAR(80) NOT NULL,
    ProcessingWindowDays INT NOT NULL,
    FeeKsh DECIMAL(12,2) NOT NULL,
    AppliesTo NVARCHAR(180) NOT NULL,
    Summary NVARCHAR(450) NOT NULL,
    Requirements NVARCHAR(500) NOT NULL,
    IsFeatured BIT NOT NULL DEFAULT 0,
    SortOrder INT NOT NULL
);
GO

CREATE TABLE dbo.Updates
(
    UpdateId INT IDENTITY(1,1) PRIMARY KEY,
    CountyId INT NULL FOREIGN KEY REFERENCES dbo.Counties(CountyId),
    Title NVARCHAR(180) NOT NULL,
    Summary NVARCHAR(400) NOT NULL,
    PublishDate DATE NOT NULL,
    Category NVARCHAR(60) NOT NULL,
    IsFeatured BIT NOT NULL DEFAULT 0
);
GO

CREATE TABLE dbo.Programs
(
    ProgramId INT IDENTITY(1,1) PRIMARY KEY,
    CountyId INT NOT NULL FOREIGN KEY REFERENCES dbo.Counties(CountyId),
    Title NVARCHAR(160) NOT NULL,
    Status NVARCHAR(30) NOT NULL,
    BudgetMillions DECIMAL(10,1) NOT NULL,
    Beneficiaries INT NOT NULL,
    Summary NVARCHAR(450) NOT NULL
);
GO

CREATE TABLE dbo.ResearchActivities
(
    ResearchActivityId INT IDENTITY(1,1) PRIMARY KEY,
    CountyId INT NULL FOREIGN KEY REFERENCES dbo.Counties(CountyId),
    Title NVARCHAR(180) NOT NULL,
    ResearchTheme NVARCHAR(90) NOT NULL,
    Status NVARCHAR(30) NOT NULL,
    LeadOffice NVARCHAR(140) NOT NULL,
    StartDate DATE NOT NULL,
    Summary NVARCHAR(450) NOT NULL,
    Outputs NVARCHAR(240) NOT NULL,
    IsFeatured BIT NOT NULL DEFAULT 0
);
GO

CREATE TABLE dbo.LicenseApplications
(
    ApplicationId INT IDENTITY(1,1) PRIMARY KEY,
    LicenseServiceId INT NOT NULL FOREIGN KEY REFERENCES dbo.LicensingServices(LicenseServiceId),
    ProjectCountyId INT NULL FOREIGN KEY REFERENCES dbo.Counties(CountyId),
    ApplicantName NVARCHAR(120) NOT NULL,
    ApplicantEmail NVARCHAR(120) NOT NULL,
    OrganizationName NVARCHAR(160) NULL,
    ProjectLocation NVARCHAR(180) NOT NULL,
    ProjectSummary NVARCHAR(1200) NOT NULL,
    SupportingDocuments NVARCHAR(500) NOT NULL,
    Status NVARCHAR(30) NOT NULL,
    ReviewNotes NVARCHAR(500) NULL,
    ReviewedAt DATETIME2 NULL,
    SubmittedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

CREATE TABLE dbo.IncidentReports
(
    ReportId INT IDENTITY(1,1) PRIMARY KEY,
    ReporterName NVARCHAR(80) NOT NULL,
    ReporterEmail NVARCHAR(120) NOT NULL,
    CountyId INT NULL FOREIGN KEY REFERENCES dbo.Counties(CountyId),
    ResponseLocationId INT NOT NULL FOREIGN KEY REFERENCES dbo.ResponseLocations(ResponseLocationId),
    Category NVARCHAR(60) NOT NULL,
    Location NVARCHAR(120) NOT NULL,
    Description NVARCHAR(1200) NOT NULL,
    Status NVARCHAR(30) NOT NULL,
    ReviewNotes NVARCHAR(500) NULL,
    UpdatedAt DATETIME2 NULL,
    ReportedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

CREATE TABLE dbo.KnowledgeDocuments
(
    DocumentId INT IDENTITY(1,1) PRIMARY KEY,
    SourceType NVARCHAR(60) NOT NULL,
    SourceRecordId INT NOT NULL,
    CountyId INT NULL FOREIGN KEY REFERENCES dbo.Counties(CountyId),
    Category NVARCHAR(90) NOT NULL,
    Title NVARCHAR(180) NOT NULL,
    Summary NVARCHAR(500) NOT NULL,
    RouteEndpoint NVARCHAR(60) NOT NULL,
    RouteRecordId INT NULL,
    NormalizedText NVARCHAR(2000) NOT NULL,
    TokenCount INT NOT NULL,
    IndexedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    CONSTRAINT UQ_KnowledgeDocuments_Source UNIQUE (SourceType, SourceRecordId)
);
GO

CREATE TABLE dbo.KnowledgeStopWords
(
    Word NVARCHAR(40) PRIMARY KEY
);
GO

CREATE TABLE dbo.KnowledgeVectorIndex
(
    DocumentId INT NOT NULL FOREIGN KEY REFERENCES dbo.KnowledgeDocuments(DocumentId),
    DimensionNumber INT NOT NULL,
    DimensionValue FLOAT NOT NULL,
    CONSTRAINT PK_KnowledgeVectorIndex PRIMARY KEY (DocumentId, DimensionNumber)
);
GO

CREATE INDEX IX_KnowledgeDocuments_Category ON dbo.KnowledgeDocuments(Category, CountyId);
CREATE INDEX IX_KnowledgeVectorIndex_Dimension ON dbo.KnowledgeVectorIndex(DimensionNumber) INCLUDE (DocumentId, DimensionValue);
CREATE INDEX IX_AdminActivityLog_OccurredAt ON dbo.AdminActivityLog(OccurredAt DESC) INCLUDE (AdminUserId, ActivityType, EntityType);
CREATE INDEX IX_IncidentReports_Status ON dbo.IncidentReports(Status, ReportedAt DESC) INCLUDE (CountyId, ResponseLocationId);
CREATE INDEX IX_LicenseApplications_Status ON dbo.LicenseApplications(Status, SubmittedAt DESC) INCLUDE (LicenseServiceId, ProjectCountyId);
GO