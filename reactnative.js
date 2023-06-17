import React, { Component } from 'react';
import { View, Text, Button } from 'react-native';
import Sound from 'react-native-sound';
import Voice from 'react-native-voice';

class PaadasML extends Component {
  constructor(props) {
    super(props);
    this.state = {
      transcription: [],
      isListening: false,
      answer: '',
      isCorrect: false,
      number: null,
      times: null,
      product: null
    };

    Sound.setCategory('Playback');
  }

  componentDidMount() {
    this.loadTranscription();
  }

  loadTranscription = () => {
    const transcription = require('./marathi_number_transcription.json');
    this.setState({ transcription });
  };

  playSound = (file) => {
    const sound = new Sound(file, Sound.MAIN_BUNDLE, (error) => {
      if (error) {
        console.log('Failed to load the sound', error);
        return;
      }
      sound.play();
    });
  };

  startListening = async () => {
    try {
      await Voice.start('mr-IN');
      this.setState({ isListening: true });
    } catch (error) {
      console.log('Error starting speech recognition', error);
    }
  };

  stopListening = async () => {
    try {
      await Voice.stop();
      this.setState({ isListening: false });
    } catch (error) {
      console.log('Error stopping speech recognition', error);
    }
  };

  handleSpeechRecognition = (e) => {
    const { error, results } = e;
    if (error) {
      console.log('Error in speech recognition', error);
      this.playSound('prompt/repeat.wav');
      return;
    }

    const answer = results && results[0] ? results[0] : '';
    console.log('Recognized answer:', answer);
    this.setState({ answer });
    this.checkAnswer(answer);
  };

  checkAnswer = (answer) => {
    const { number, times } = this.state;
    const product = number * times;
    const numberTranscriptions = this.state.transcription[product - 1];
    const isCorrect = numberTranscriptions.includes(answer);

    this.setState({ isCorrect }, () => {
      if (isCorrect) {
        this.playSound('prompt/correct.wav');
      } else {
        this.playSound('prompt/incorrect.wav');
        this.playSound(numbers/${answer}.wav);
        this.playSound('prompt/incorrect.wav');
      }

      setTimeout(() => {
        this.reviseProblem();
      }, 1000);
    });
  };

  reviseProblem = () => {
    const { number, times, product } = this.state;
    this.playSound(`numbers/${number}.wav
