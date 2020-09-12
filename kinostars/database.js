import firestore from '@react-native-firebase/firestore';

const stars = await firestore()
  .collection('stars')
  .get();

// const user = await firestore()
//   .collection('Users')
//   .doc('ABC')
//   .get();
