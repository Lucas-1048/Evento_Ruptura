import { useEffect, useState } from "react";
import axios from "axios";
import {
  Box,
  Input,
  VStack,
  HStack,
  Text,
  Avatar,
  Flex,
  Icon,
  CloseButton,
  InputGroup,
  InputRightElement,
} from "@chakra-ui/react";
import { FaComments } from "react-icons/fa";

import { HiMiniPaperAirplane } from "react-icons/hi2";

async function sendRequest(mensagem) {
  const url = "http://127.0.0.1:5000/process";

  try {
    const response = await axios.post(
      url,
      {
        message: mensagem,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    return [response.data.response, false];
  } catch (error) {
    console.error("Erro ao enviar a mensagem:", error);

    const errorMessage =
      error.response?.data?.error ||
      "Erro ao realizar pergunta, tente novamente mais tarde";

    return [errorMessage, true];
  }
}

function ChatApp() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isChatOpen, setIsChatOpen] = useState(false);

  let botColor = "whiteAlpha.900";

  useEffect(() => {
    async function sendInitialMessage() {
      const [answer] = await sendRequest(
        "Você é um chatbot da Localiza. Agora pergunte o nome do usuário."
      );
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: answer, sender: "bot", color: botColor },
      ]);
    }

    sendInitialMessage();
  }, []);

  const handleSendMessage = async () => {
    if (inputValue.trim()) {
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          text: inputValue,
          sender: "user",
          color: "customColors.orange",
        },
      ]);
      setInputValue("");

      const [answer, error] = await sendRequest(inputValue);

      if (error) {
        botColor = "red.400";
      }

      setMessages((prevMessages) => [
        ...prevMessages,
        { text: answer, sender: "bot", color: botColor },
      ]);
    }
  };

  const toggleChat = () => {
    setIsChatOpen((prevState) => !prevState);
  };

  return (
    <div>
      {!isChatOpen && (
        <Box
          as="button"
          position="fixed"
          bottom="20px"
          right="20px"
          w="60px"
          h="60px"
          bg="customColors.orange"
          borderRadius="full"
          boxShadow="lg"
          display="flex"
          alignItems="center"
          justifyContent="center"
          _hover={{ bg: "customColors.orange" }}
          onClick={toggleChat}
        >
          <Icon as={FaComments} boxSize="24px" color="white" />
        </Box>
      )}

      {isChatOpen && (
        <Box
          border="1px solid"
          borderColor="gray.200"
          borderRadius="28px"
          overflow="hidden"
          position="fixed"
          bottom="20px"
          right="20px"
          bg="customColors.lightGray"
        >
          {/* Chat Header */}
          <Flex
            bg="customColors.lightGray"
            p="4"
            color="white"
            align="center"
            justify="space-between"
          >
            <Avatar size="sm" name="Chatbot" />
            <Text fontSize="lg" color="customColors.darkGray">
              Chatbot
            </Text>
            <CloseButton
              size="sm"
              color="customColors.darkGray"
              onClick={toggleChat}
            />
          </Flex>

          <VStack
            p="4"
            spacing="3"
            overflowY="scroll"
            align="flex-start"
            w="36rem"
            h="36rem"
          >
            {messages.map((message, index) => (
              <HStack
                key={index}
                w="full"
                justify={message.sender === "user" ? "flex-end" : "flex-start"}
              >
                <Box
                  bg={message.color}
                  color={
                    message.sender === "user" || message.color === "red.400"
                      ? "whiteAlpha.900"
                      : "customColors.darkGray"
                  }
                  px="4"
                  py="2"
                  borderTopLeftRadius="3xl"
                  borderTopRightRadius={
                    message.sender === "user" ? "none" : "3xl"
                  }
                  borderBottomLeftRadius={
                    message.sender === "user" ? "3xl" : "none"
                  }
                  borderBottomRightRadius="3xl"
                  maxW="80%"
                >
                  <Text>{message.text}</Text>
                </Box>
              </HStack>
            ))}
          </VStack>

          <HStack p="3">
            <InputGroup marginBottom="0.5rem">
              <Input
                placeholder="Olá, chat!"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                bg="whiteAlpha.900"
                borderRadius="3xl"
                focusBorderColor="transparent"
                border="none"
                _hover={{ boxShadow: "none" }}
                boxShadow="lg"
              />
              <InputRightElement>
                <Box
                  as={HiMiniPaperAirplane}
                  color="customColors.orange"
                  size="1.25rem"
                  marginRight="4px"
                />
              </InputRightElement>
            </InputGroup>
          </HStack>
        </Box>
      )}
    </div>
  );
}

export default ChatApp;
