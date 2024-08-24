

const studyPopup = Vue.createApp({


  data() {
    return {
      category: NaN,
      showNSPopup: false,
      showSSPopup: false,
      showWSPopup: false,
      showSizesList: true,
      showTimesList: false,
      sizes: [3, 5, 8, 10, 15],
      times: [1,3, 5, 10, 12, 20],
      selectedOption: 'size',
      selectedValue: 3
    }
  },
  mounted() {
    console.log(list_id)
    // this.list_id = this.props;
    // console.log(this.$props)
  },
  methods: {
    resetValues(){
     this.selectedOption = 'size'
      this.selectedValue = 3
    },
    changeCategory(value) {
     this.category = value
    },
    showSizes() {
      this.showSizesList = true
      this.showTimesList = false
      this.selectedOption = 'size'
      this.selectedValue = 5
    },
    showTimes() {
      this.showTimesList = true
      this.showSizesList = false
      this.selectedOption = 'time'
      this.selectedValue = 5
    },
    selectOption(option, value) {
      this.selectedOption = option
      this.selectedValue = value
    },

    postToNewPage(url) {
      // Create a form element
      let form = document.createElement("form");
      form.method = "POST";
      form.action = url;

      // Add data to the form
          let input = document.createElement("input");
          input.type = "hidden";
          input.name = this.selectedOption;
          input.value = this.selectedValue;
          let list_id_input  = document.createElement("input");
          list_id_input.type = "hidden";
          list_id_input.name = 'list_id';
          list_id_input.value = list_id;
          let category_input = document.createElement("input");
          category_input.type = "hidden";
          category_input.name = 'category';
          category_input.value = this.category;
          form.appendChild(input);
          form.appendChild(list_id_input);
          form.appendChild(category_input);

      // Append the form to the body and submit it
      document.body.appendChild(form);
      form.submit();
    },
    openNSPopUp() {
      this.category = 'ns'
      this.resetValues()
     this.showNSPopup = true
      this.showWSPopup = false
      this.showSSPopup = false
    },
    openWSPopUp() {
      this.category = 'ws'
      this.resetValues()
     this.showNSPopup = false
      this.showWSPopup = true
      this.showSSPopup = false
    },
    openSSPopUp() {
      this.category = 'ss'
      this.resetValues()
     this.showNSPopup = false
      this.showWSPopup = false
      this.showSSPopup = true
    },
    closeNSPopUp(){
      this.showNSPopup = false
     this.resetValues()
    },
    closeWSPopUp(){
      this.showWSPopup = false
     this.resetValues()
    },
     closeSSPopUp(){
      this.showSSPopup = false
     this.resetValues()
    },

    start() {
      // Use this.selectedOption and this.selectedValue here

      console.log(`You selected ${this.selectedOption} with value ${this.selectedValue}`)
      console.log(this.list_id)
      this.postToNewPage('/character/recognition_practice');
      this.resetValues()
    }
  },
  delimiters:['[[',']]']
})


studyPopup.mount('#studyPopup')