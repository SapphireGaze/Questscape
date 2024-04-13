import express from "express";

import { Quest } from "../lib/types";

import QuestModel from "../models/quest.model";

const PlayRouter: express.Router = express.Router();

PlayRouter.use(express.json());

PlayRouter.get("/:id", async (req: express.Request, res: express.Response) => {
  try {
    const _id: string = req.params.id;
    const quest: Quest | null = await QuestModel.findById(_id).exec();

    res.status(200).json(quest);
  } catch (err) {
    res.status(501).json({ error: (err as Error).message });
  }
});

export default PlayRouter;
