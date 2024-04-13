import express from "express";

import QuestModel from "../models/quest.model";

const CreateRouter: express.Router = express.Router();

CreateRouter.use(express.json());

CreateRouter.post("/", async (req: express.Request, res: express.Response) => {
  try {
    const { waypoints } = req.body;

    const newQuest = await new QuestModel({
      waypoints: waypoints,
    }).save();

    const _id = newQuest._id;

    res.status(200).json({ _id: `${_id}` });
  } catch (err) {
    res.status(501).json({ error: (err as Error).message });
  }
});

export default CreateRouter;
