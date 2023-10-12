const Ballot = artifacts.require("Ballot");

module.exports = function(deployer) {
  // Define an array of bytes32 proposal names
  const proposalNames = [
    web3.utils.utf8ToHex("Proposal 1"),
    web3.utils.utf8ToHex("Proposal 2"),
    web3.utils.utf8ToHex("Proposal 3")
  ]; // Add your proposal names here

  // Deploy the Ballot contract with the proposalNames array as the constructor argument
  deployer.deploy(Ballot, proposalNames);
};

