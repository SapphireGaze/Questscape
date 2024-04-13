import mongoose, { Schema, Types } from "mongoose";

import { Waypoint } from "../lib/types";

const WaypointSchema: mongoose.Schema = new Schema<Waypoint>({
  latitude: {
    type: Number,
    required: true,
  },
  longitude: {
    type: Number,
    required: true,
  },
  clue: {
    type: String,
    required: true,
  },
});

const WaypointModel: mongoose.Model<Waypoint> = mongoose.model<Waypoint>(
  "Waypoint",
  WaypointSchema
);

export { WaypointSchema, WaypointModel };
