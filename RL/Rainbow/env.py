# -*- coding: utf-8 -*-
from collections import deque
import random
import socket
import json
import torch

from AdditionalScripts.action_space import generate_action_space
from AdditionalScripts.frame_processor import dump_pixel_data

class Env():
  def __init__(self, args):
    self.device = args.device
    self.actions = generate_action_space()
    self.window = args.history_length  # Number of frames to concatenate
    self.state_buffer = deque([], maxlen=args.history_length)
    # Wait to make initial connection to dolphin client
    host = socket.gethostname()
    port = 5555
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(1)
    self.client_socket, _ = sock.accept()

  def _get_state(self):
    message = json.loads(self.client_socket.recv(131072).decode('utf-8'))
    reward = message[1] #reward function value
    done = message[2] # termination flag
    frame = message[3] # frame counter
    observation = dump_pixel_data(frame_index=frame) #pixel values
    return torch.tensor(observation, dtype=torch.float32, device=self.device).div_(255), reward, done, frame

  def _reset_buffer(self):
    for _ in range(self.window):
      self.state_buffer.append(torch.zeros(84, 84, device=self.device))

  def reset(self):
    self.client_socket.send( ( json.dumps( (_, True) ).encode("utf-8") ) )
    self._reset_buffer()
    observation, _, _, _ = self._get_state()
    self.state_buffer.append(observation)
    return torch.stack(list(self.state_buffer), 0)

  def step(self, action):
    self.client_socket.send( ( json.dumps( (self.actions[action], False) ).encode("utf-8") ) )
    observation, reward, done, frame = self._get_state() # json.loads(self.client_socket.recv(131072).decode('utf-8'))
    self.state_buffer.append(observation)
    return torch.stack(list(self.state_buffer), 0), reward, done, frame

  def action_space(self):
    return len(self.actions)

  def close(self):
    self.client_socket.close()