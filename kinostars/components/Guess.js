import React, {Component} from 'react';
import {
  Alert,
  Image,
  View,
  StyleSheet
} from 'react-native';
import { Button } from 'react-native-elements';
import Icon from 'react-native-vector-icons/FontAwesome';


import storage from '@react-native-firebase/storage';
import firestore from '@react-native-firebase/firestore';

const reference = storage().ref('/images/5.jpg');

const levels = [{
  options: ['Some name', 'Name Surname', 'Another name', 'Last name'],
  answer: 'Name Surname',
  image: reference,
},
{
  options: ['Some name 2', 'Name Surname 2', 'Another name 2', 'Last name 2'],
  answer: 'Name Surname 2',
  image: reference,
}];

class Guess extends Component {
  state = {
    level: 0,
    image: null,
    options: [],
    answer: '',
    buttons: [],
  };

  checkOption(event, optionSelected) {
    // Alert.alert('Calling my function')
    this.setState((state) => {
      let newButtons = [];
      state.buttons.forEach((button) => {
        if(button.props.title === optionSelected) {
          const icon = optionSelected === state.answer ? 'check-circle' : 'times-circle';
          const selectedButton = (<Button
            title={optionSelected}
            key={optionSelected}
            type='outline'
            style={styles.button}
            icon={
              <Icon
                name={icon}
                size={30}
              />
            }
          />);
          newButtons.push(selectedButton);
        } else {
          const disabledButton = (<Button
            title={button.props.title}
            key={button.props.title}
            type='outline'
            style={styles.button}
            disabled
          />);
          newButtons.push(disabledButton);
        }
      });
      state.buttons = newButtons;
      return state;
    });
    // Add transition animation
    setTimeout(() => {this.nextLevel()}, 1000)
  };

  async loadStar(levelIndex) {
    const options = levels[levelIndex].options;
    const answer = levels[levelIndex].answer;
    const imageRef = levels[levelIndex].image;
    const image = await imageRef.getDownloadURL();
    const stars = await firestore()
    .collection('stars')
    .get();
    stars.forEach((elem) => {
      console.log(elem.data());
    })
    // console.log('This is image', image);
    buttons = options.map(choice => (
      <Button
        title={choice}
        key={choice}
        type='outline'
        onPress={(event) => this.checkOption(event, choice)}
        style={styles.button}
      />)
    );
    this.setState({
      image: image,
      answer: answer,
      buttons: buttons
    });

  }

  nextLevel() {
    const newLevel = this.state.level + 1;
    if(newLevel >= levels.length) {
      Alert.alert('End of the game');
      return
    }

    this.setState({
      level: newLevel
    });
    this.loadStar(newLevel);
  }

  async componentDidMount() {
    await this.loadStar(this.state.level);
  }

  render(props) {
    return (
      <View style={styles.imageContainer}>
        <Image
          style={[{width: 360, height: 570}, styles.image]}
          source={{uri: this.state.image}}
        />
        {this.state.buttons}
      </View>
    );
  }
}

const styles = StyleSheet.create({
  button: {
    marginTop: 5,
    marginLeft: 10,
    marginRight: 10,
  },
  imageContainer: {
    // flex: 1
  },
  image: {
    borderRadius: 15,
  }
});

export default Guess;
