import { Button, Card, List } from "antd";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { Urls } from "../../constant/Urls";
import { CreateRequest, GetGames } from "../../services/api/game/game.service";
import Pusher from 'pusher-js';

const GameList = () => {
  const navigate = useNavigate();
  const [games, setGames] = useState([]);
  const pusher = new Pusher('77369da9d48e78083d81', {
    cluster: 'ap2'
  });

  useEffect(() => {
    getGames();
  }, []);
  useEffect(()=>{
    const channel = pusher.subscribe('lobby');
    channel.bind('all-games', function() {
      getGames();
    });
    return ()=>{
        pusher.unsubscribe('lobby');
    }
  },[games]);

  // useEffect(() => {
  //   const subscribeToGameChannel = (gameId) => {
  //     const channel = pusher.subscribe(`game-channel-${gameId}`);

  //     channel.bind('join-request', (data) => {
  //       setNotifications(prev => [...prev, data]);
  //     });

  //     return () => {
  //       pusher.unsubscribe(`game-channel-${gameId}`);
  //     };
  //   };

  //   // Unsubscribe from all previously subscribed channels
  //   games.forEach(game => {
  //     pusher.unsubscribe(`game-channel-${game.game_id}`);
  //   });

  //   // Subscribe to channels for all fetched games
  //   games.forEach(game => {
  //     subscribeToGameChannel(game.game_id);
  //   });

  //   // Clean up on component unmount
  //   return () => {
  //     games.forEach(game => {
  //       pusher.unsubscribe(`game-channel-${game.game_id}`);
  //     });
  //   };
  // }, [games]);

  const getGames = async () => {
    try {
      const response = await GetGames();
      // console.log(response)
      setGames(response.data);
    } catch (err) {
      console.error("Error fetching the Games:", err);
    }
  };

  const requestToJoin = async (gameId) => {
    try {
      // Your join game request logic here
      const joinRequest= await CreateRequest({game_id:gameId})
      console.log('Request to join game', gameId);
    } catch (error) {
      console.error(error);
    }
  };

 

  return (
    <div className="container flex flex-col flex-grow p-4 mx-auto mb-5 align-items-center">
      <div className="flex items-center justify-between">
        <h1 className="mt-5 mb-4 text-2xl font-bold text-center">Games available</h1>
        <Button type="primary" onClick={() => navigate(Urls.Games.NewGame())}>
          Create
        </Button>
      </div>
      <List
        grid={{ gutter: 16, column: 1 }}
        dataSource={games}
        renderItem={(game) => (
          <List.Item>
            <Card title={`${game.game_name}`} className="shadow-lg d-flex">
              <p className="text-lg">Owner: {game.owner}</p>
              <p className="text-lg">Status: {game.status}</p>
              <div className="flex justify-end gap-4">
                <Button type="primary" onClick={() => requestToJoin(game.game_id)}>
                  Join
                </Button>
              </div>
            </Card>
          </List.Item>
        )}
      />
    </div>
  );
};

export default GameList;
