// js/firebase-config.js

// Firebase Configuration untuk WarungPudding
const firebaseConfig = {
  apiKey: "AIzaSyAOEoUtCrDJHT3f-o2PaIlM4oOIjjztdc4",
  authDomain: "warungpudding.firebaseapp.com",
  databaseURL: "https://warungpudding-default-rtdb.firebaseio.com",
  projectId: "warungpudding",
  storageBucket: "warungpudding.firebasestorage.app",
  messagingSenderId: "987094779569",
  appId: "1:987094779569:web:624c7ec9214079d5528490",
  measurementId: "G-HYSWZH5KRD"
};

// Inisialisasi Firebase (menggunakan versi compat CDN)
firebase.initializeApp(firebaseConfig);
const db = firebase.database();
console.log("Firebase Realtime Database terhubung secara Real-Time!");
