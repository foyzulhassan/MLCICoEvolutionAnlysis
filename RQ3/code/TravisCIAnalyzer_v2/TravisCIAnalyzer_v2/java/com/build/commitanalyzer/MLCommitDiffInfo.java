package com.build.commitanalyzer;

import com.opencsv.bean.CsvBindByName;
import com.opencsv.bean.CsvBindByPosition;
import com.opencsv.bean.CsvCustomBindByName;

public class MLCommitDiffInfo {
	
	@CsvBindByPosition(position = 0, required = true)
	@CsvBindByName(column = "GitAuthor", required = true)
	private String gitAuthor;
	@CsvBindByPosition(position = 1, required = true)
	@CsvBindByName(column = "ProjectName", required = true)
	private String projName;
	@CsvBindByPosition(position = 2, required = true)
	@CsvBindByName(column = "CommitID", required = true)
	private String commitID;
	@CsvBindByPosition(position = 3, required = false)
	@CsvBindByName(column = "CommitMessage", required = false)
	private String commitMessage;
	@CsvBindByPosition(position = 5, required = false)
	@CsvBindByName(column = "LinesAdded", required = false)
	private int linesAdded;
	@CsvBindByPosition(position = 6, required = false)
	@CsvBindByName(column = "LinesRemoved", required = false)
	private int linesRemoved;
	@CsvBindByPosition(position = 7, required = false)
	@CsvBindByName(column = "LinesModified", required = false)
	private int linesModified;
	@CsvBindByPosition(position = 8, required = false)
	@CsvBindByName(column = "TravisASTDiff", required = false)
	private String travisAstDiffStr;
	@CsvBindByPosition(position = 9, required = false)
	@CsvBindByName(column = "PythonASTDiff", required = false)
	private String pythonAstDiffStr;
	@CsvBindByPosition(position = 10, required = false)
	@CsvBindByName(column = "PythonFilesChanged", required = false)
	private int pythonFilesChanged;
	@CsvBindByPosition(position=11 ,required=false)
	@CsvBindByName(column = "failure reason", required=false)
	private String failureReason;
	@CsvBindByPosition(position=12,required=false)
	@CsvBindByName(column = "envMapDiffPath",required=false)
	private String envMapDiffPath;
	@CsvBindByPosition(position =13,required=false)
	@CsvBindByName(column = "debug",required=false)
	private String debug;
	
	
	public String getDebug() {
		return debug;
	}

	public void setDebug(String debug) {
		this.debug = debug;
	}

	public String getEnvMapDiffPath() {
		return envMapDiffPath;
	}

	public void setEnvMapDiffPath(String envMapDiffPath) {
		this.envMapDiffPath = envMapDiffPath;
	}

	public String getFailureReason() {
		return failureReason;
	}

	public void setFailureReason(String failureReason) {
		this.failureReason = failureReason;
	}

	public String getGitAuthor() {
		return gitAuthor;
	}
	
	public void setGitAuthor(String gitAuthor) {
		this.gitAuthor = gitAuthor;
	}

	public String getProjName() {
		return projName;
	}

	public void setProjName(String projName) {
		this.projName = projName;
	}

	public String getCommitID() {
		return commitID;
	}

	public void setCommitID(String commitID) {
		this.commitID = commitID;
	}

	public String getCommitMessage() {
		return commitMessage;
	}

	public void setCommitMessage(String commitMessage) {
		this.commitMessage = commitMessage;
	}


	public int getLinesAdded() {
		return linesAdded;
	}

	public void setLinesAdded(int linesAdded) {
		this.linesAdded = linesAdded;
	}

	public int getLinesRemoved() {
		return linesRemoved;
	}

	public void setLinesRemoved(int linesRemoved) {
		this.linesRemoved = linesRemoved;
	}

	public int getLinesModified() {
		return linesModified;
	}

	public void setLinesModified(int linesModified) {
		this.linesModified = linesModified;
	}
	
	public String getTravisAstDiffStr() {
		return travisAstDiffStr;
	}
	
	public void setTravisAstDiffStr(String travisAstDiffStr) {
		this.travisAstDiffStr = travisAstDiffStr;
	}
	
	public String getPythonAstDiffStr() {
		return pythonAstDiffStr;
	}
	
	public void setPythonAstDiffStr(String pythonAstDiffStr) {
		this.pythonAstDiffStr = pythonAstDiffStr;
	}
	
	public int getPythonFilesChanged() {
		return pythonFilesChanged;
	}
	
	public void setPythonFilesChanged(int pythonFilesChanged) {
		this.pythonFilesChanged = pythonFilesChanged;
	}
}
