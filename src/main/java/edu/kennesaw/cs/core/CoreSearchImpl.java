package edu.kennesaw.cs.core;

import edu.kennesaw.cs.readers.Document;

import java.util.*;

/*
This class is an example implementation of the CoreSearch, you can either modify or write another implementation of the Core Search.
 */

/**
 * Created by Ferosh Jacob
 * Date: 01/27/18
 * KSU: CS 7263 Text Mining
 */
public class CoreSearchImpl implements CoreSearch {


    Map<String, List<Integer>> invertedIndex = new HashMap<String, List<Integer>>();

    Map<String, Map<Integer, Integer>> invertedIndex_freq = new HashMap<String, Map<Integer, Integer>>();



//    Map<Integer, Integer> docFreq = new HashMap<Integer, Integer>();

    public void init() {

    }

    /*
    A very simple tokenization.
     */
    public String[] tokenize(String title) {
        return title.split(" ");
    }

    public void addToIndex(Document document) {

        String[] tokens = tokenize(document.getTitle());
        for (String token : tokens) {
            addTokenToIndex(token, document.getId());
        }

    }

    private void addTokenToIndex(String token, int docId) {

        if (invertedIndex.containsKey(token)) {
            List<Integer> docIds = invertedIndex.get(token);
            docIds.add(docId);
            Collections.sort(docIds);
            invertedIndex.put(token, docIds);


            // Update Doc Frequency Hash
            updateDocFreq(token,docId);



        } else {
            List<Integer> docIds = new ArrayList<Integer>();
            docIds.add(docId);
            invertedIndex.put(token, docIds);


            // add token to doc frequency
            invertedIndex_freq.put(token, new HashMap<Integer, Integer>( docId, 1  ));
        }


    }

    private void updateDocFreq(String token,  int docId ){
        if(invertedIndex_freq.get(token).containsKey(docId)){
            int val = invertedIndex_freq.get(token).get(docId).intValue();
            invertedIndex_freq.get(token).put(docId, val + 1);

        } else {
            invertedIndex_freq.get(token).put(docId, 1);
        }
    }
    private int getDocFreq(String token,  int docId ){

        int freq = 0;
        if(invertedIndex_freq.get(token).containsKey(docId)){
            freq = invertedIndex_freq.get(token).get(docId).intValue();
        }
        return freq;
    }

    private int getInvertedListSize( ){
        return invertedIndex.size();
    }

    /*
    A very simple search implementation.
     */


    /*
    Ignore terms in query that are not in Index
     */
    private String[] removeNotIndexTokens(String[] split) {
        List<String> indexedTokens = new ArrayList<String>();
        for (String token : split) {
            if (invertedIndex.containsKey(token)) indexedTokens.add(token);
        }
        return indexedTokens.toArray(new String[indexedTokens.size()]);
    }







    /*
    A very simple search implementation.
     */
    public List<Integer> search(String query) {
        String[] queryTokens = removeNotIndexTokens(query.split(" "));
        List<Integer> mergedDocIds = new ArrayList<Integer>();
        if (queryTokens.length == 0) return mergedDocIds;
        int index = 1;
        if (queryTokens.length == 1)
            invertedIndex.get(queryTokens[0]);

        List<Integer> initial = invertedIndex.get(queryTokens[0]);
        while (index < queryTokens.length) {
            initial = mergeTwoDocIds(initial, invertedIndex.get(queryTokens[index]));
            index++;
        }

        return initial;
    }

    /*
    AND Merging postings!!
     */
    public List<Integer> mergeTwoDocIds(List<Integer> docList1, List<Integer> docList2) {
        int docIndex1 = 0;
        int docIndex2 = 0;
        List<Integer> mergedList = new ArrayList<Integer>();
        List<Integer> vip = new ArrayList<Integer>();
        while (docIndex1 < docList1.size() && docIndex2 < docList2.size()) {
            if (docList1.get(docIndex1).intValue() == docList2.get(docIndex2).intValue()) {
                int value = docList1.get(docIndex1).intValue();
                boolean found = false;
                mergedList.add(docList1.get(docIndex1));


                docIndex1++;
                docIndex2++;
            } else if (docList1.get(docIndex1) < docList2.get(docIndex2)) {
                mergedList.add(docList1.get(docIndex1));

                docIndex1++;
            } else if (docList1.get(docIndex1) > docList2.get(docIndex2)) {
                mergedList.add(docList2.get(docIndex2));

                docIndex2++;
            }
        }


        return mergedList;
    }


}








//   Returns in ranked order
//
//
//    public List<Integer> search(String query) {
//        String[] queryTokens = removeNotIndexTokens(query.split(" "));
//        List<Integer> mergedDocIds = new ArrayList<Integer>();
//        Map<Integer, Integer> occurence = new HashMap<Integer, Integer>();
//
//
//
//        if (queryTokens.length == 0) return mergedDocIds;
//        int index = 1;
//        if (queryTokens.length == 1)
//            invertedIndex.get(queryTokens[0]);
//
//
//        // Create list
//        List<Integer> interm = invertedIndex.get(queryTokens[0]);
//
//        // Remove Dup doc
//        List<Integer> initial = new ArrayList<Integer>();
//        initial.add(interm.get(0));
//        for (int i = 1; i <  interm.size(); i++) {
//            if(initial.get(initial.size() - 1) != interm.get(i))
//                initial.add(interm.get(i));
//        }
//
//        // Num of occurences
//        for (int i = 0; i < initial.size() ; i++) {
//            occurence.put(initial.get(i), 1);
//        }
//
//
//        while (index < queryTokens.length) {
//            initial = mergeTwoDocIds(initial, invertedIndex.get(queryTokens[index]), occurence);
//            index++;
//        }
//
//        List<Integer> results = new ArrayList<Integer>();
//        results.add(initial.get(0));
//        for (int i = 0; i < initial.size(); i++) {
//            int docID = initial.get(i);
//            int freq = occurence.get(docID).intValue();
//
//            int j= 0;
//            while (results.size() > j &&   occurence.get(results.get(j)) < freq){
//                j++;
//            }
//
//            results.add(docID);
//
//
//        }
//
//
//        return results;
//    }
//
//
//    public List<Integer> mergeTwoDocIds(List<Integer> docList1, List<Integer> docList2, Map<Integer, Integer> occurence) {
//        int docIndex1 = 0;
//        int docIndex2 = 0;
//        List<Integer> mergedList = new ArrayList<Integer>();
//        List<Integer> vip = new ArrayList<Integer>();
//        while (docIndex1 < docList1.size() && docIndex2 < docList2.size()) {
//            if (docList1.get(docIndex1).intValue() == docList2.get(docIndex2).intValue()) {
//                int docID = docList1.get(docIndex1);
//                mergedList.add(docID);
//
//
//                int freq = occurence.get(docID).intValue();
//                occurence.put(docID, freq +1);
//
//                docIndex1++;
//                docIndex2++;
//            } else if (docList1.get(docIndex1) < docList2.get(docIndex2)) {
//                mergedList.add(docList1.get(docIndex1));
//
//                docIndex1++;
//            } else if (docList1.get(docIndex1) > docList2.get(docIndex2)) {
//                int docID = docList2.get(docIndex2);
//                mergedList.add(docID);
//
//                docIndex2++;
//
//                if (occurence.containsKey(docID)){
//                    int freq = occurence.get(docID).intValue();
//                    occurence.put(docID, freq +1);
//                } else {
//                    occurence.put(docID, 1);
//                }
//            }
//        }
//
//
//        return mergedList;
//    }
//




//  Original

//    public List<Integer> mergeTwoDocIds(List<Integer> docList1, List<Integer> docList2) {
//        int docIndex1 = 0;
//        int docIndex2 = 0;
//        List<Integer> mergedList = new ArrayList<Integer>();
//        while (docIndex1 < docList1.size() && docIndex2 < docList2.size()) {
//            if (docList1.get(docIndex1).intValue() == docList2.get(docIndex2).intValue()) {
//                mergedList.add(docList1.get(docIndex1));
//                docIndex1++;
//                docIndex2++;
//            } else if (docList1.get(docIndex1) < docList2.get(docIndex2)) {
//                docIndex1++;
//            } else if (docList1.get(docIndex1) > docList2.get(docIndex2)) {
//                docIndex2++;
//            }
//        }
//
//        return mergedList;
//    }


