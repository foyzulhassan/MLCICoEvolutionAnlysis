package com.ghadiff;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.build.commitanalyzer.CommitAnalyzer;
import com.build.commitanalyzer.MLCommitDiffInfo;
import com.config.Config;
import com.github.gumtreediff.actions.EditScript;
import com.github.gumtreediff.actions.model.Action;
import com.github.gumtreediff.actions.model.Addition;
import com.github.gumtreediff.actions.model.Delete;
import com.github.gumtreediff.actions.model.Insert;
import com.github.gumtreediff.actions.model.Move;
import com.github.gumtreediff.actions.model.TreeAddition;
import com.github.gumtreediff.actions.model.TreeDelete;
import com.github.gumtreediff.actions.model.TreeInsert;
import com.github.gumtreediff.actions.model.Update;
import com.github.gumtreediff.tree.ITree;
import com.github.gumtreediff.tree.TreeUtils;
import com.opencsv.CSVWriter;
import com.travis.parser.BashCmdAnalysis;
import com.travisdiff.TravisCIChangeBlocks;
import com.utility.NodeLabelWrapper;

import edu.util.fileprocess.CSVReaderWriter;
import edu.util.fileprocess.CVSReader;

public class GHACIDiffGenMngr{

public void generateGHACIChangeData() {
    // CSVReaderWriter csvrw = new CSVReaderWriter();
    CVSReader csvreader = new CVSReader();
    String csvPath = Config.csvCITransitionFile;  // Path to CSV containing commit data

    try {
        CSVReaderWriter readWrite = new CSVReaderWriter();
        File file = new File(Config.rootDir + "debug_map_presence_gha.csv"); 
        FileWriter outputfile = new FileWriter(file); 
        CSVWriter writer = new CSVWriter(outputfile);

        // Read commit diff info from CSV
        List<MLCommitDiffInfo> diffInfos = readWrite.getMLCommitDiffInfoFromCSV(csvPath);
        List<String[]> mapPresenceData = new ArrayList<String[]>();

        System.out.println("diffinfos");
        System.out.println(diffInfos);
        System.out.println("mappresencedata");
        System.out.println(mapPresenceData);

        // Generate GitHub Actions change blocks
        TravisCIChangeBlocks changeblocks = ghaCIDiffGenerate(diffInfos, mapPresenceData);

        // Write command presence data to CSV
        writer.writeAll(mapPresenceData);

        // Generate statistics based on the changes
        generateStatOnChangeBlock(changeblocks);

        writer.close();
    } catch (Exception e) {
        e.printStackTrace();
    }
}

public TravisCIChangeBlocks ghaCIDiffGenerate(List<MLCommitDiffInfo> mlDiffInfo, List<String[]> mapPresenceData) {

	TravisCIChangeBlocks changeblocks = new TravisCIChangeBlocks();  // Renamed for GHA
    int id = 1;
    int count = 0;
    String[] headers = {"commandPresence", "ChangePresence", "projectName", "commit"};
    mapPresenceData.add(headers);
    List<String[]> actionsDebug = new ArrayList<String[]>();
    System.out.println(mlDiffInfo);

    for (MLCommitDiffInfo entry : mlDiffInfo) {
        CommitAnalyzer cmtanalyzer = null;
        System.out.println("test id==>" + id);
        id++;

        try {
            String gitUrl = "https://github.com/" + entry.getProjName() + ".git";
            System.out.println(gitUrl);
            cmtanalyzer = new CommitAnalyzer(entry.getProjName().split("/")[0], entry.getProjName().split("/")[1], gitUrl);

            // Extract GHA workflow file changes instead of Travis CI file changes
            EditScript actions = cmtanalyzer.extractGHAFileChangesFromSingleCommit(entry.getCommitID());  // Changed method name
            System.out.print("actions - "+actions.toString());
            System.out.print("commitid - "+entry.getCommitID());
            CommitAnalyzer.CommandMaps commandPresenceMap = cmtanalyzer.nodeInFile_for_gha(entry.getCommitID(), Arrays.asList(Config.gha_nodesToLookForAsArray));

            // Create row for mapPresenceData based on command presence and change presence maps
            String[] row = {commandPresenceMap.getPresenceMap().toString(), commandPresenceMap.getChangePresenceMap().toString(), entry.getProjName(), entry.getCommitID()};
            mapPresenceData.add(row);

            if (actions != null) {
                count++;
                for (Action action : actions) {
                    ITree treenode = action.getNode();
                    String jsonblock = (String) treenode.getMetadata("json_parent");
                    String label = getNodeLabel(treenode);
                    String straction = "";

                    // Handle different action types (add, delete, update, etc.)
                    if (action instanceof TreeDelete) {
                        straction = "Tree-Delete";
                    } else if (action instanceof TreeAddition) {
                        straction = "Tree-Addition";
                    } else if (action instanceof TreeInsert) {
                        straction = "Tree-Insert";
                    } else if (action instanceof Move) {
                        straction = "Move";
                    } else if (action instanceof Update) {
                        straction = "Update";
                    } else if (action instanceof Insert) {
                        straction = "Insert";
                    } else if (action instanceof Addition) {
                        straction = "Addition";
                    } else if (action instanceof Delete) {
                        straction = "Delete";
                    } else {
                        System.out.println("Undefined behavior");
                    }

                    // Analyze the specific commands/changes inside GitHub Actions workflows
                    List<String> changecmd = getCmdListFromChange(jsonblock, label);

                    // Wrap the node data and add to the change blocks
                    NodeLabelWrapper nodelabel = new NodeLabelWrapper(treenode, label, straction, action, changecmd, entry.getCommitID(), entry.getProjName());
                    changeblocks.addItemToMap(jsonblock, nodelabel);
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    System.out.println("Total Diffs=" + count);
    return changeblocks;
}

public List<String> getCmdListFromChange(String changeblock, String changestr) {

    // Define GitHub Actions blocks to track (no direct 'before_script' in GitHub Actions)
//    List<String> allowedBlocks = new ArrayList<>();

    // Common sections of GitHub Actions workflows
//    allowedBlocks.add("jobs");
//    allowedBlocks.add("steps");
//    allowedBlocks.add("run");
//    allowedBlocks.add("on");
//    allowedBlocks.add("name");
//    allowedBlocks.add("uses");
//    allowedBlocks.add("env");
//    allowedBlocks.add("permissions");
//    allowedBlocks.add("if");
//    allowedBlocks.add("with");
//    allowedBlocks.add("secrets");
//    allowedBlocks.add("strategy");
//    allowedBlocks.add("matrix");
//    allowedBlocks.add("timeout-minutes");
//    allowedBlocks.add("continue-on-error");

    String str = changestr.trim();

    // Remove GitHub Actions-specific sections from the change string
    if (str.startsWith("name:")) {
        str = str.replace("name:", "").trim();
    }
    if (str.startsWith("run-name:")) {
        str = str.replace("run-name:", "").trim();
    }
    if (str.startsWith("env:")) {
        str = str.replace("env:", "").trim();
    }
    if (str.startsWith("defaults:")) {
        str = str.replace("defaults:", "").trim();
    }

    if (str.startsWith("concurrent:")) {
        str = str.replace("concurrent:", "").trim();
    }

    if (str.startsWith("jobs:")) {
        str = str.replace("jobs:", "").trim();
    }
    if (str.startsWith("steps:")) {
        str = str.replace("steps:", "").trim();
    }
    if (str.startsWith("run:")) {
        str = str.replace("run:", "").trim();
    }
    if (str.startsWith("on:")) {
        str = str.replace("on:", "").trim();
    }
    if (str.startsWith("uses:")) {
        str = str.replace("uses:", "").trim();
    }
    if (str.startsWith("env:")) {
        str = str.replace("env:", "").trim();
    }
    if (str.startsWith("permissions:")) {
        str = str.replace("permissions:", "").trim();
    }
    if (str.startsWith("if:")) {
        str = str.replace("if:", "").trim();
    }
    if (str.startsWith("with:")) {
        str = str.replace("with:", "").trim();
    }
    if (str.startsWith("secrets:")) {
        str = str.replace("secrets:", "").trim();
    }
    if (str.startsWith("strategy:")) {
        str = str.replace("strategy:", "").trim();
    }
    if (str.startsWith("matrix:")) {
        str = str.replace("matrix:", "").trim();
    }
//    if (str.startsWith("timeout-minutes:")) {
//        str = str.replace("timeout-minutes:", "").trim();
//    }
//    if (str.startsWith("continue-on-error:")) {
//        str = str.replace("continue-on-error:", "").trim();
//    }

    // Normalize certain commands, for instance converting 'pip3' to 'pip'
    if (str.equals("pip3")) {
        str = "pip";
    }

    // Analyze the bash commands, if any, within the GitHub Actions workflow
    BashCmdAnalysis bashcmdanalysis = new BashCmdAnalysis();
    Map<String, String> envmap = new HashMap<>();

    // Analyze the cleaned string for bash commands
    List<String> basecmds = bashcmdanalysis.getBashCommandTreeFromChange(str, envmap);

    return basecmds;
}

public void generateStatOnChangeBlock(TravisCIChangeBlocks changeblocks) {  // Renamed for GHA
    Map<String, List<NodeLabelWrapper>> changeList = changeblocks.getChangeList();

    Writer statsFileWriter = null;
    Writer outputFileWriter = null;

    // Update file paths to reflect GHA analysis
    String statsFile = Config.rootDir+"gha_output_statistical_analysis_expanded_keys_total_keys_stats.csv";
    String outputFile = Config.rootDir+"\\gha_output_statistical_analysis_expanded_keys_v3.csv";
    
    CSVWriter outputFileCsvWriter = null;
    CSVWriter statsFileCsvWriter = null;

    try {
        // Prepare the output file writers
        outputFileWriter = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(outputFile, true), "utf-8"));
        outputFileCsvWriter = new CSVWriter(outputFileWriter);
        String[] headers = {"action", "key", "label", "cmdString", "projectName", "commitId"};  // Same headers
        statsFileWriter = new OutputStreamWriter(new FileOutputStream(statsFile, true), "utf-8");
        statsFileCsvWriter = new CSVWriter(statsFileWriter);
        outputFileCsvWriter.writeNext(headers);  // Write the headers to the CSV
    } catch (IOException ex) {
        System.out.println(ex.getMessage());
    }

    // Iterate through each change block in the change list
    for (String key : changeList.keySet()) {
        List<NodeLabelWrapper> nodelabel = changeList.get(key);

        // Write detailed change data to output CSV
        for (NodeLabelWrapper node : nodelabel) {
            String[] row = {node.getStrAction(), key, node.getLabel(), node.getCmdsString(), node.getProjectName(), node.getCommitId()};
            outputFileCsvWriter.writeNext(row);  // Write the change information to the CSV
        }

        // Write summary stats about each block to stats CSV
        String[] otherRow = {key, "" + nodelabel.size()};
        statsFileCsvWriter.writeNext(otherRow);  // Write block name and size to stats CSV
        System.out.println("Block Name==>" + key + "   Size==>" + nodelabel.size());
    }

    try {
        outputFileCsvWriter.close();
        statsFileCsvWriter.close();
    } catch (IOException e) {
        e.printStackTrace();
    }
}



public String getNodeLabel(ITree node) {
//	StringBuilder strbuild = new StringBuilder();
//
//	strbuild.append(node.getLabel());
//	List<ITree> children = node.getChildren();
//
//	for (ITree child : children) {
//		strbuild.append(child.getLabel());
//	}
//
//	return strbuild.toString();
	List<ITree> allnodes = TreeUtils.preOrder(node);
	StringBuilder strbuild = new StringBuilder();

	// strbuild.append(node.getLabel());

	boolean isfiled = false;

	if (node.getType().toString().equals("FIELD")) {
		isfiled = true;
	}

	for (ITree child : allnodes) {
		String childlabel = child.getLabel();
		if (child.getType().toString().equals("FIELD")) {
			isfiled = true;
		}
		if (childlabel != null && childlabel.length() > 0) {

			childlabel = childlabel.replaceFirst("\"", "");
			int last = childlabel.lastIndexOf('\"');
			if (last > 0 && last < childlabel.length()) {
				childlabel = childlabel.substring(0, last);
			}

			if (isfiled) {
				strbuild.append(childlabel + ":");
				isfiled = false;
			} else {
				strbuild.append(childlabel + " ");
			}
		}

	}

	String strlabel = strbuild.toString();
	strlabel = strlabel.trim();
	// System.out.println(strlabel);
	return strlabel;

}

}


