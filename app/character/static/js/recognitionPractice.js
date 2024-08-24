console.log(charactersDataJson)
const recognitionPractice = Vue.createApp({
  data() {
    return {
        timeLength: parseInt(timeLength),
        timeRemaining: NaN,
      characters: JSON.parse(charactersDataJson), // array of character objects from backend
      studiedChars: [],
        progressPercent: 0,
      patternedChars: undefined,
      currentCharacterIndex: 0,
        showDetailsVisible: false,
        practiceDone: false,
        // submittingData: false,

    };
  },
  computed: {
    currentCharacter() {
      return this.patternedChars[this.currentCharacterIndex];
    }
  },
    mounted(){
      if(this.currentCharacter.isCorrect){
          this.showDetailsVisible = false
      }

    }
    ,
    created(){
      if(!isNaN(this.timeLength)){
          this.countdownTimer(timeLength, this.submitAnswers)
      }
    },
  beforeMount() {

    this.characters = [...this.characters.map(value => {
      return {...value, isCorrect:false, charState: 'new'}
    })]
    this.patternedChars = this.generatePattern(this.characters, 3)
},
  methods: {
      countdownTimer(minutes, callback) {
  let totalSeconds = minutes * 60;
  let intervalId = setInterval(() => {
    let secondsRemaining = totalSeconds;
    let minutesRemaining = Math.floor(totalSeconds / 60);
    let seconds = totalSeconds % 60;
     this.timeRemaining = minutesRemaining >= 0 ? `${minutesRemaining}:${String(seconds).padStart(2, '0')}` : `${seconds} seconds`;
    this.progressPercent = ((minutes * 60 - secondsRemaining) / (minutes * 60)) * 100;
    console.log(totalSeconds, secondsRemaining)
    console.log(this.progressPercent);
    // this.progressPercent = this.progressPercent.toFixed(2)
    console.log(`Time remaining: ${this.timeRemaining}`);
    // console.log(`Progress: ${this.progressPercent.toFixed(2)}%`);
    totalSeconds--;
    if (totalSeconds < 0) {
      clearInterval(intervalId);
      callback();
    }
  }, 1000); // update every 1 second
},
//        countdownTimer(minutes, callback) {
//   let totalSeconds = minutes * 60;
//   let intervalId = setInterval(() => {
//     let secondsRemaining = totalSeconds;
//     let minutesRemaining = Math.floor(totalSeconds / 60);
//     let seconds = totalSeconds % 60;
//     this.timeRemaining = minutesRemaining > 0 ? `${minutesRemaining}:${String(seconds).padStart(2, '0')}` : `${seconds} seconds`;
//     console.log(`Time remaining: ${this.timeRemaining}`);
//     totalSeconds--;
//     this.progressPercent = (to / this.characters.length) * 100;
//
//     if (totalSeconds <= 0) {
//       clearInterval(intervalId);
//       callback();
//     }
//   }, 1000); // update every 1 second
// },
//        generatePattern(arr) {
//   const result = [];
//   for (let i = 0; i < arr.length; i++) {
//     // Add the original element
//     result.push(arr[i]);
//
//     // Add elements from the next subarray (but skip out-of-bounds indices)
//     for (let j = i + 1; j < Math.min(i + 3, arr.length); j++) {
//       result.push(arr[j]);
//     }
//   }
//   console.log(result)
//   return result;
// },
          generatePattern(arr) {
  const result = [];
  const cycleSize = 3; // adjust this value to change the cycle size

  for (let i = 0; i < cycleSize; i++) {
    result.push(arr[i]);
  }

  for (let i = 0; i < arr.length - cycleSize; i++) {
    result.push(arr[i]);
    result.push(arr[i + cycleSize]);
  }

  for (let i = arr.length - cycleSize; i < arr.length; i++) {
    result.push(arr[i]);
  }

  console.log(result);
  return result;
},



 nextCharacter() {
     this.currentCharacterIndex++
     if(this.currentCharacterIndex === this.patternedChars.length){
         this.submitAnswers()
     }

   if(!this.studiedChars.includes(this.patternedChars[this.currentCharacterIndex])){
      this.studiedChars.push(this.currentCharacter);
      if(isNaN(this.timeLength)){
          this.progressPercent = (this.studiedChars.length / this.characters.length) * 100;
      }
   }
   console.log(this.studiedChars)


},

    markDone(characterId) {
      this.currentCharacter.isCorrect = true
        this.currentCharacter.charState = 'done';
      this.nextCharacter()
    },

      markForgot(characterId) {
       this.currentCharacter.isCorrect = false
          this.currentCharacter.charState = 'new';
       this.nextCharacter()
      },

    markCorrect(characterId) {
      this.currentCharacter.isCorrect = true
        this.showDetailsVisible = false
      this.nextCharacter()
    },

    markIncorrect(characterId) {
      this.currentCharacter.isCorrect = false
        this.showDetailsVisible = false
      this.nextCharacter()

    },

    showDetails(){
      this.showDetailsVisible = true
    },

    submitAnswers() {
          this.practiceDone = true
        let dataToSend = this.studiedChars.map(value => {
            return {character_id: value.id, is_correct:value.isCorrect}
        })
      fetch('/character/update_chars_detail', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dataToSend)
      })
      .then(response => response.json())
      .then(data => {
        this.$router.push('/report');
      })
      .catch(error => {
        console.error(error);
      });
    },
  },
  delimiters: ['[[',']]'],
})

recognitionPractice.mount('#recognitionPractice')