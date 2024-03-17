--These steps derived from code at https://github.com/michaelgorkow/scs_whisper/tree/main

USE ROLE RL_TEAM_JENKINS;
USE SCHEMA DB_TEAM_JENKINS.KL_TEST_JENKINS;

CREATE STAGE IF NOT EXISTS WHISPER_MODELS ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE') DIRECTORY = (ENABLE = TRUE);
CREATE STAGE IF NOT EXISTS AUDIO_FILES ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE') DIRECTORY = (ENABLE = TRUE);
CREATE STAGE IF NOT EXISTS WHISPER_APP ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE') DIRECTORY = (ENABLE = TRUE);

SHOW IMAGE REPOSITORIES;


-- Note, that Michael Gorkow uses the base openai-whisper package. This will attempt to download and cache models models on first use from openai servers. With external access configuration, that is blcoked in spcs.
-- Instead, using the process described here to downlaod the model locally for offline use: https://github.com/openai/whisper/discussions/1463, got download links from https://github.com/openai/whisper/blob/main/whisper/__init__.py.  

-- ## Setup Instructions
-- ### 1. Create image repository, stages and compute pool 
-- ```sql
-- -- create image repository
-- CREATE OR REPLACE IMAGE REPOSITORY TEST_IMAGE_REPOSITORY;

-- ### 3. Build & Upload the container
-- ```cmd
--docker build --platform linux/amd64 -t ahsorg-ahsprod.registry.snowflakecomputing.com/db_team_jenkins/kl_test_jenkins/kl_jenkins_repository/whisper_app:latest https://github.com/lonergan123/scs_whisper.git
--docker login ahsorg-ahsprod.registry.snowflakecomputing.com -u SVC_TEAM_JENKINS
--docker push ahsorg-ahsprod.registry.snowflakecomputing.com/db_team_jenkins/kl_test_jenkins/kl_jenkins_repository/whisper_app:latest
;
--download whisper base model manually
--from https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt
--and upload to WHISPER_MODELS stage

PUT 'file://c:\\Users\\klonergan\\Downloads\\tiny.en.pt' '@WHISPER_MODELS' AUTO_COMPRESS=false OVERWRITE=true;
PUT 'file://c:\\Users\\klonergan\\Downloads\\tiny.pt' '@WHISPER_MODELS' AUTO_COMPRESS=false OVERWRITE=true;
PUT 'file://c:\\Users\\klonergan\\Downloads\\base.en.pt' '@WHISPER_MODELS' AUTO_COMPRESS=false OVERWRITE=true;
PUT 'file://c:\\Users\\klonergan\\Downloads\\base.pt' '@WHISPER_MODELS' AUTO_COMPRESS=false OVERWRITE=true;
PUT 'file://c:\\Users\\klonergan\\Documents\\MyVSCodeRepo\\scs_whisper\\spec.yml' '@WHISPER_APP' AUTO_COMPRESS=false OVERWRITE=true;
PUT 'file://c:\\Users\\klonergan\\Documents\\MyVSCodeRepo\\scs_whisper\\test_stage_file.txt' '@WHISPER_APP' AUTO_COMPRESS=false OVERWRITE=true;
PUT 'file://c:\\Users\\klonergan\\Downloads\\SampleMedDictation.mp3' '@AUDIO_FILES' AUTO_COMPRESS=false OVERWRITE=true;

--Confirm files in stage
LIST @AUDIO_FILES;

--Create/ Alter Whisper Service
CREATE SERVICE WHISPER_APP
    IN COMPUTE POOL tutorial_compute_pool --for now, just use CPU compute pool for testing
    FROM @WHISPER_APP
    SPEC = 'spec.yml'
    MIN_INSTANCES=1
    MAX_INSTANCES=1;


-- Confirm service is running
SHOW SERVICES;
SELECT SYSTEM$GET_SERVICE_STATUS('WHISPER_APP');
SHOW ENDPOINTS IN SERVICE WHISPER_APP;

-- Error logs
CALL SYSTEM$GET_SERVICE_LOGS('WHISPER_APP', '0', 'whisper-service-container', 10);
--To connect to service from python, get public endpoint ingress url


-- CREATE OR REPLACE FUNCTION DETECT_LANGUAGE(AUDIO_FILE TEXT, ENCODE BOOLEAN)
-- RETURNS VARIANT
-- SERVICE=WHISPER_APP
-- ENDPOINT=API
-- AS '/detect-language';

-- Function to transcribe audio files
-- CREATE OR REPLACE FUNCTION TRANSCRIBE(TASK TEXT, LANGUAGE TEXT, AUDIO_FILE TEXT, ENCODE BOOLEAN)
-- RETURNS VARCHAR
-- SERVICE=WHISPER_APP
-- ENDPOINT=API
-- AS '/asr';

-- Run Whisper on a files in a stage
-- SELECT RELATIVE_PATH, 
--        GET_PRESIGNED_URL('@AUDIO_FILES', RELATIVE_PATH) AS PRESIGNED_URL,
--        DETECT_LANGUAGE(PRESIGNED_URL,True)  AS WHISPER_RESULTS,
--        WHISPER_RESULTS['detected_language']::text as DETECTED_LANGUAGE
-- FROM DIRECTORY('@AUDIO_FILES');

SELECT RELATIVE_PATH, 
       GET_PRESIGNED_URL('@AUDIO_FILES', 'german_texts/') AS PRESIGNED_URL,
       TRANSCRIBE('transcribe','',PRESIGNED_URL,True) AS WHISPER_RESULTS,
       WHISPER_RESULTS['text']::TEXT as EXTRACTED_TEXT
FROM DIRECTORY('@AUDIO_FILES');