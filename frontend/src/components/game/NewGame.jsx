import { Button, Card, Form, Input, InputNumber, Select } from "antd";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { Urls } from "../../constant/Urls";
import { CreateGame } from "../../services/api/game/game.service";
import moment from "moment";

const { Option } = Select;

const NewGame = () => {
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const createGame = async (data) => {
    try {
      const response = await CreateGame(data);
      toast.success("Game created successfully!");
      navigate(Urls.Games.Games());
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFinish = (values) => {
    setLoading(true);

    // Convert duration into seconds (assuming expiration_time is in seconds)
    const durationInSeconds = values.duration * {
      hours: 3600,
      minutes: 60,
      seconds: 1,
    }[values.unit];

    const data = {
      game_name: values.name,
      expiration_time: durationInSeconds, // Store the duration as seconds in the backend
    };
    createGame(data);
  };

  return (
    <div className="container flex flex-col items-center justify-center flex-grow p-4 mx-auto mb-5">
      <h1 className="mt-5 mb-4 text-2xl font-bold text-center">Create Game</h1>
      <Card className="w-full shadow-lg lg:w-1/2">
        <Form form={form} layout="vertical" onFinish={handleFinish}>
          <Form.Item
            label="Game Name"
            name="name"
            rules={[{ required: true, message: "Please input the game name!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Expiration Time"
            required
          >
            <Input.Group compact>
              <Form.Item
                name="duration"
                noStyle
                rules={[{ required: true, message: "Please enter the duration!" }]}
              >
                <InputNumber min={1} placeholder="Duration" />
              </Form.Item>
              <Form.Item
                name="unit"
                noStyle
                rules={[{ required: true, message: "Please select the unit!" }]}
              >
                <Select placeholder="Select Unit">
                  <Option value="hours">Hours</Option>
                  <Option value="minutes">Minutes</Option>
                  <Option value="seconds">Seconds</Option>
                </Select>
              </Form.Item>
            </Input.Group>
          </Form.Item>
          <Form.Item className="mb-0">
            <div className="flex justify-between w-full">
              <Button type="" onClick={() => navigate(Urls.Games.Games())}>
                Cancel
              </Button>
              <Button type="primary" htmlType="submit" loading={loading}>
                Save
              </Button>
            </div>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default NewGame;
