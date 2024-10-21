package com.config;

import java.io.File;

public class Config {
	// public static String rootDir="/media/AutoBuilder/UnityPerformance/";
	 //public static String
	 //rootDir=".\\Project_Data";

	 //Set to the project root folder, in wherever your TravisCIAnalyzer is
	 public static String
	 rootDir="C:\\paper\\co_evolution_analysis\\RQ3\\data\\code_generated\\";
	 
	 //repo dir location for caching repos
	 public static String repoDir = "C:\\paper\\empirical_analysis\\data\\repos\\";
	 //
	 //text file that contains list of projects to analyze
	 public static String gitProjList=rootDir+"github_links.txt";
	 public static String gitProjListNonML=rootDir+"Project_Source_NonML.txt";
	 public static String gitProjListEval=rootDir+"eval_Project_Source.txt";
	
	 //reporDir used for storing Unity Projects
	 public static String repoDirEval= rootDir+"EvalRepos/"; /*rootDir+"GitRepo/";*/	 
	 public final static String[] nodesToLookForAsArray = {"script","install","before_install","after_install","after_success","before_script",
			 "deploy","before_deploy"
             ,"after_deploy","after_failure","before_failure","after_script","before_cache",
             "after_sucess"};

	 public final static String[] gha_nodesToLookForAsArray = {    
			    "on", "jobs", "env", 
			    "job_name", "runs-on", "strategy", "matrix", "needs", "environment", "concurrency",
			    "steps", "name", "run", "uses", "shell", "working-directory", "continue-on-error", "with",
			    "permissions", "defaults", "if", "secrets", "services",
			    "deploy", "restore-keys", "save-keys", "cache", "timeout-minutes",
			    "on_success", "on_failure", "always",
			    "outputs", "condition"
			};
	 
		public static String travisRepoDir = "/home/alaa/alexis-project/CloneWithGetPy/travisData";
	
	 public static String csvFile=rootDir+"perf_commit_data_Updated.csv";
	 
	 public static String csvFreqFile=rootDir+"new_new_cmd_frequency_non_ml_unique.csv";
	 
	 public static String csvCmdTypeFile=rootDir+"command_type_new_ML_Non_Ml.csv";
	 
	 //public static String csvCITransitionFile=rootDir+"Tool_transition.csv";
	 public static String csvCITransitionFile="C:\\paper\\co_evolution_analysis\\RQ3\\data\\cleaned_ci_modifying_commits";
	 
	 public static String csvBlockCategory=Config.rootDir+"block_type.csv";
			 
	 public static String patchDir=rootDir+"PatchDir/";

	public static String[] perfCommitToken = { ".." };

	public static int commitid = 1;
	public static int stmtUniqueId = 1;
	
	/**This value controls the maximum number of files in a commit before the LoC/AST analysis task skips it.<br>
	 * This can be set to Integer.MAX_VALUE to include all files. Note that doing so will likely make the analysis take substantially longer.*/
	public static final int maxPythonFiles = Integer.MAX_VALUE; //was 30
	
	/** This token expires at the end of 2023, and should be replaced with a token from whoever is working on this then. 
	 * 
	 * To create a secure token like this, go to Github, click your profile picture, and go to 
	 * Settings > Developer Settings > Personal Access Token > Fine-Grained tokens.
	 * 
	 * Only set the required permissions. Cloning public repositories needs only read access to public repositories, making this the only requirement for at least task 14. 
	 * 
	 * Github accounts can also be used directly, if 2FA is off, but are not recommended. 
	 */
	public static String gitHubUserName="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";
	public static String gitHubPwd="";
	
	public static String[] compoundcmds= {"python","bash", "source", "python3", "sh", "eval", "xvfb-run", "/bin/bash",
			"doit","ruby","unbuffer","catchsegv"};
	
	public static String repoStrDate="08-10-2021";

}