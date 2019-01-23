module.exports = {
  networks: {
    live: {
      host: "localhost",
      port: 8545,
      network_id: 1
    },
    test: {
      host: "localhost",
      port: 8546,
      network_id: 15
    },
     ropsten:  {
     network_id: 3,
     host: "localhost",
     port:  8546,
     gas:   29000
   }
  },
   rpc: {
     host: 'localhost',
     post:8545
  },
  mocha: {
    enableTimeouts: false
  }

};
