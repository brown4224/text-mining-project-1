package edu.kennesaw.cs.core;

public class ScoreCard {
    private int docID;
    private int occurence;
    private int score;


    public ScoreCard(int docID, int score) {
        this.docID = docID;
        this.occurence = 1;
        this.score = score;
    }

    public int getDocID() {
        return docID;
    }

    public void setDocID(int docID) {
        this.docID = docID;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public void addScore(int score) {
        this.score += score;
    }

    public void incrOccurence(){
        this.occurence++;
    }

    public int getOccurence(){
        return this.occurence;
    }

}
