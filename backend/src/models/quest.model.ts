import mongoose, { Schema } from "mongoose";

import { Quest } from "../lib/types";

import { WaypointSchema } from "./waypoint.model";

const QuestSchema: mongoose.Schema = new Schema<Quest>({
  waypoints: [WaypointSchema],
});

const QuestModel: mongoose.Model<Quest> = mongoose.model<Quest>(
  "Quest",
  QuestSchema
);

export default QuestModel;
