import firestore from '@react-native-firebase/firestore';

const stars = await firestore()
  .collection('stars')
  .get();
