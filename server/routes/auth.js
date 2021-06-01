import express from "express";
import axios from "axios";

const router = express.Router();

const getAccountFor = async (address) => {
  const config = {
    headers: {
      accept: "application/json",
    },
  };
  const REQUEST_URL = `https://testnet.algoexplorerapi.io/idx2/v2/accounts/${address}`;

  try {
    const request = await axios.get(REQUEST_URL, config);
    let walletOwnerData = await request.data;

    return {
      data: walletOwnerData,
    };
  } catch (errInfo) {
    // Handle Error Here
    console.error(errInfo);
    return {
      error: errInfo,
    };
  }
};

router.post("/login", async (req, res) => {
  const body = req.body;
  let walletAddress = body.address;

  const result = await getAccountFor(walletAddress);
  let responseObj = result.data
    ? { data: result.data }
    : { error: result.error }; // if error, error key is returned, if successful then data key is returned

  res.status(200).json(responseObj);
});

router.post("/signup", async (req, res) => {
  const body = req.body;
  const { firstName, lastName, walletAddress, password } = body;

  const accountData = await getAccountFor(walletAddress);

  if (accountData.data) {
    let result = {
      ...accountData,
      algoEtf: { firstName: firstName, lastName: lastName, password: password },
    };

    // dump into MongoDB
    // TODO

    res.status(200).json(result);
  } else {
    res.status(200).json({ error: "Wallet Address does not exist." });
  }
});

router.patch("/forgot-password", async (req, res) => {
  res.json({
    message: "Hi from forgot password",
  });
});

export default router;
